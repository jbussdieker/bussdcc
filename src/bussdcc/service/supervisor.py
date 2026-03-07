import threading
import traceback
from dataclasses import dataclass
from typing import Dict, List

from bussdcc.context.protocol import ContextProtocol
from bussdcc.service.protocol import ServiceProtocol
from bussdcc.message import service as message

from .info import ServiceInfo


@dataclass
class _ServiceEntry:
    service: ServiceProtocol
    attached: bool = False
    running: bool = False
    thread: threading.Thread | None = None
    stop_event: threading.Event | None = None


class ServiceSupervisor:
    def __init__(self, ctx: ContextProtocol):
        self._ctx = ctx
        self._services: Dict[str, _ServiceEntry] = {}
        self._lock = threading.RLock()

    def register(self, service: ServiceProtocol) -> None:
        with self._lock:
            if service.name in self._services:
                raise ValueError(f"Service `{service.name}` already registered")

            self._services[service.name] = _ServiceEntry(service=service)

    def names(self) -> list[str]:
        with self._lock:
            return list(self._services)

    def list(self) -> list[ServiceProtocol]:
        with self._lock:
            return [entry.service for entry in self._services.values()]

    def get(self, name: str) -> ServiceProtocol | None:
        with self._lock:
            entry = self._services.get(name)
            return entry.service if entry else None

    def status(self, name: str) -> ServiceInfo:
        with self._lock:
            entry = self._services[name]

            return ServiceInfo(
                name=entry.service.name,
                running=entry.running,
                enabled=entry.service.enabled,
                attached=entry.attached,
                interval=entry.service.interval,
                restart=entry.service.restart,
                critical=entry.service.critical,
            )

    def statuses(self) -> List[ServiceInfo]:
        with self._lock:
            return [
                ServiceInfo(
                    name=e.service.name,
                    running=e.running,
                    enabled=e.service.enabled,
                    attached=e.attached,
                    interval=e.service.interval,
                    restart=e.service.restart,
                    critical=e.service.critical,
                )
                for e in self._services.values()
            ]

    def boot(self) -> None:
        with self._lock:
            for entry in self._services.values():
                if not entry.attached:
                    try:
                        entry.service.attach(self._ctx)
                        entry.attached = True
                    except Exception as e:
                        self._ctx.emit(
                            message.ServiceFailure(
                                service=entry.service.name,
                                error=repr(e),
                                traceback=traceback.format_exc(),
                            )
                        )

            for name in self._services:
                self._start_locked(name)

    def stop_all(self) -> None:
        with self._lock:
            names = list(self._services)
        for name in names:
            self.stop(name)

    def start(self, name: str) -> None:
        with self._lock:
            self._start_locked(name)

    def is_running(self, name: str) -> bool:
        with self._lock:
            entry = self._services.get(name)
            return bool(entry and entry.running)

    def running(self) -> List[ServiceProtocol]:
        with self._lock:
            return [entry.service for entry in self._services.values() if entry.running]

    def stop(self, name: str) -> None:
        with self._lock:
            entry = self._services[name]

            if not entry.running:
                return

            assert entry.stop_event is not None
            assert entry.thread is not None

            entry.stop_event.set()

        thread = entry.thread

        if thread:
            thread.join()

        entry.service.stop(self._ctx)

        with self._lock:
            entry.running = False
            entry.thread = None
            entry.stop_event = None

    def enable(self, name: str) -> None:
        with self._lock:
            entry = self._services[name]
            entry.service.enabled = True

    def disable(self, name: str) -> None:
        with self._lock:
            entry = self._services[name]
            entry.service.enabled = False
            running = entry.running

        if running:
            self.stop(name)

    def shutdown(self) -> None:
        self.stop_all()

        with self._lock:
            services = list(self._services.values())

        for entry in services:
            try:
                entry.service.detach()
            except Exception as e:
                self._ctx.emit(
                    message.ServiceError(
                        service=entry.service.name,
                        error=repr(e),
                        traceback=traceback.format_exc(),
                    )
                )

    def _start_locked(self, name: str) -> None:
        """Caller must hold self._lock."""
        entry = self._services[name]

        if not entry.service.enabled or entry.running:
            return

        stop_event = threading.Event()

        thread = threading.Thread(
            target=self._run_service,
            name=f"svc:{name}",
            args=(entry, stop_event),
            daemon=True,
        )

        entry.thread = thread
        entry.stop_event = stop_event
        entry.running = True

        thread.start()

        self._ctx.emit(message.ServiceStarted(service=name))

    def _run_service(
        self,
        entry: _ServiceEntry,
        stop_event: threading.Event,
    ) -> None:
        svc = entry.service
        ctx = self._ctx

        try:
            svc.start(ctx)

            while not stop_event.is_set():

                try:
                    svc.tick(ctx)

                except Exception as e:
                    ctx.emit(
                        message.ServiceError(
                            service=svc.name,
                            error=repr(e),
                            traceback=traceback.format_exc(),
                        )
                    )

                    if svc.critical:
                        ctx.emit(
                            message.ServiceFailure(
                                service=svc.name,
                                error=repr(e),
                                traceback=traceback.format_exc(),
                            )
                        )
                        break

                    if not svc.restart:
                        break

                    ctx.emit(message.ServiceRestart(service=svc.name))

                ctx.clock.sleep(svc.interval, cancel=stop_event)
        finally:
            with self._lock:
                entry.running = False

            ctx.emit(message.ServiceStopped(service=svc.name))
