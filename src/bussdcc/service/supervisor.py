from typing import Dict
import threading
import traceback

from bussdcc.context import ContextProtocol

from .protocol import ServiceProtocol


class ServiceSupervisor:
    """
    Orchestrates services: start, tick, stop, and restart.
    """

    def __init__(self, ctx: ContextProtocol):
        self.ctx = ctx
        self._services: Dict[str, ServiceProtocol] = {}
        self._threads: Dict[str, threading.Thread] = {}
        self._stop_flag = threading.Event()

    def register(self, service: ServiceProtocol) -> None:
        self._services[service.name] = service

    def start_all(self) -> None:
        self._stop_flag.clear()
        for service in self._services.values():
            self._start_service(service)

    def stop_all(self) -> None:
        self._stop_flag.set()
        for service in self._services.values():
            service.stop(self.ctx)

        # Wait for threads to exit
        for t in self._threads.values():
            t.join()
        self._threads.clear()

    def _start_service(self, service: ServiceProtocol) -> None:
        def runner() -> None:
            while not self._stop_flag.is_set():
                try:
                    service.start(self.ctx)
                    while (
                        getattr(service, "enabled", True)
                        and not self._stop_flag.is_set()
                    ):
                        service.tick(self.ctx)
                        self.ctx.clock.sleep(getattr(service, "interval", 1.0))
                except Exception as e:
                    self.ctx.events.emit(
                        "service.error",
                        service=service.name,
                        error=repr(e),
                        traceback=traceback.format_exc(),
                    )
                    if getattr(service, "critical", False):
                        self.ctx.events.emit(
                            "service.critical_failure",
                            service=service.name,
                            error=repr(e),
                        )
                        # Critical failure halts supervisor
                        self._stop_flag.set()
                        break

                    if getattr(service, "restart", True):
                        self.ctx.events.emit(
                            "service.restart",
                            service=service.name,
                        )
                        continue  # restart the loop
                    else:
                        break
                finally:
                    service.stop(self.ctx)
                    self.ctx.events.emit("service.stopped", service=service.name)

        t = threading.Thread(target=runner, name=f"service:{service.name}", daemon=True)
        self._threads[service.name] = t
        t.start()
        self.ctx.events.emit("service.started", service=service.name)
