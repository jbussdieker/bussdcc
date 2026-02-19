from typing import Optional, Dict, Self, Type, Literal
from types import TracebackType

from bussdcc.context import Context, ContextProtocol
from bussdcc.clock import Clock, SystemClock
from bussdcc.device import DeviceProtocol
from bussdcc.event import Event, EventEngine, EventEngineProtocol
from bussdcc.state import StateEngine, StateEngineProtocol
from bussdcc.service import ServiceProtocol, ServiceSupervisor
from bussdcc.process import ProcessProtocol
from bussdcc.version import get_version

from .protocol import RuntimeProtocol
from .sink import EventSinkProtocol


class Runtime(RuntimeProtocol):
    def __init__(
        self,
        *,
        clock: Optional[Clock] = None,
        events: EventEngineProtocol | None = None,
        state: StateEngineProtocol | None = None,
    ):
        self.clock: Clock = clock or SystemClock()
        self.events: EventEngineProtocol = events or EventEngine(clock=self.clock)
        self.state: StateEngineProtocol = state or StateEngine()
        self._sinks: list[EventSinkProtocol] = []
        self._devices: Dict[str, DeviceProtocol] = {}
        self._services: Dict[str, ServiceProtocol] = {}
        self._processes: Dict[str, ProcessProtocol] = {}
        self._interfaces: Dict[str, ProcessProtocol] = {}
        # type-safe context using RuntimeProtocol
        self.ctx: ContextProtocol = Context(
            clock=self.clock, runtime=self, events=self.events, state=self.state
        )
        self._booted: bool = False
        self.version: str = get_version()
        self._service_supervisor: ServiceSupervisor | None = None

    def _on_boot(self) -> None:
        """Hook for subclasses to initialize resources."""
        return None

    def _on_shutdown(self, reason: Optional[str] = None) -> None:
        """Hook for subclasses to release resources."""
        return None

    def _dispatch(self, evt: Event) -> None:
        for sink in self._sinks:
            try:
                sink.handle(evt)
            except Exception as e:
                if evt.name != "runtime.sink.failure":
                    self.events.emit(
                        "runtime.sink.failure", sink=type(sink).__name__, error=repr(e)
                    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} booted={self._booted}>"

    def __enter__(self) -> Self:
        self.boot()

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Literal[False]:
        reason = None
        if exc_type is not None:
            reason = f"{exc_type.__name__}: {exc_val}"
        self.shutdown(reason=reason)

        # Returning False allows exceptions to propagate normally
        return False

    @property
    def booted(self) -> bool:
        return self._booted

    def add_sink(self, sink: EventSinkProtocol) -> None:
        if self._booted:
            raise RuntimeError("Cannot add sinks after boot")
        self._sinks.append(sink)

    def register_service(self, service: ServiceProtocol) -> None:
        if self._booted:
            raise RuntimeError("Cannot register services after boot")
        self._services[service.name] = service

    def register_process(self, process: ProcessProtocol) -> None:
        if self._booted:
            raise RuntimeError("Cannot register processes after boot")
        self._processes[process.name] = process

    def register_interface(self, interface: ProcessProtocol) -> None:
        if self._booted:
            raise RuntimeError("Cannot register interfaces after boot")
        self._interfaces[interface.name] = interface

    def attach_device(self, device: DeviceProtocol) -> None:
        """
        Attach a device to the runtime.

        - If called before boot(), the device is staged and attached during boot.
        - If called after boot(), the device is attached immediately.
        """
        if device.id in self._devices:
            raise ValueError(f"Device {device.id} already attached")

        if not self._booted:
            self._devices[device.id] = device
            return

        device.attach(self.ctx)
        self._devices[device.id] = device

    def detach_device(self, id: str) -> None:
        device = self._devices.pop(id, None)
        if not device:
            return
        device.detach()

    def get_device(self, id: str) -> DeviceProtocol | None:
        return self._devices.get(id)

    def list_devices(self, *, kind: str | None = None) -> list[DeviceProtocol]:
        if kind is None:
            return list(self._devices.values())
        return [d for d in self._devices.values() if d.kind == kind]

    def boot(self) -> None:
        if self._booted:
            return

        self._sub = self.events.subscribe(self._dispatch)

        for sink in self._sinks:
            sink.start(self.ctx)

        self.ctx.events.emit("runtime.booting", version=self.version)

        self._on_boot()

        # Boot all registered devices
        for device in self._devices.values():
            device.attach(self.ctx)

        # Attach processes
        for process in self._processes.values():
            process.attach(self.ctx)
            process.start(self.ctx)
            self.ctx.events.emit("process.started", process=process.name)

        # Attach interfaces
        for interface in self._interfaces.values():
            interface.attach(self.ctx)
            interface.start(self.ctx)
            self.ctx.events.emit("interface.started", interface=interface.name)

        self._booted = True
        self.ctx.events.emit("runtime.booted", version=self.version)

        # Start services under supervisor
        self._service_supervisor = ServiceSupervisor(self.ctx)
        for service in self._services.values():
            service.attach(self.ctx)
            self._service_supervisor.register(service)

        self._service_supervisor.start_all()

    def shutdown(self, reason: Optional[str] = None) -> None:
        if not self._booted:
            return  # Be idempotent on shutdown to avoid exit crashes

        try:
            self.ctx.events.emit("runtime.shutting_down", reason=reason)

            # Stop services first then detach
            if self._service_supervisor:
                self._service_supervisor.stop_all()

            for service in self._services.values():
                service.detach()

            # Stop and detach interfaces
            for interface in self._interfaces.values():
                try:
                    interface.stop(self.ctx)
                finally:
                    interface.detach()
                    self.ctx.events.emit("interface.stopped", interface=interface.name)

            # Stop and detach processes
            for process in self._processes.values():
                try:
                    process.stop(self.ctx)
                finally:
                    process.detach()
                    self.ctx.events.emit("process.stopped", process=process.name)

            # Detach devices in reverse order
            for device in reversed(list(self._devices.values())):
                device.detach()

            self._on_shutdown(reason)

            self.ctx.events.emit("runtime.shutdown", version=self.version)

            self._sub.cancel()

            for sink in reversed(self._sinks):
                sink.stop()
        except Exception:
            raise
        finally:
            # Ensure state is reset even if on_shutdown fails
            self._booted = False
