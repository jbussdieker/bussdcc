from typing import Optional, Dict, Self, Type, Literal
from types import TracebackType

from bussdcc.context import Context, ContextProtocol
from bussdcc.clock import Clock, SystemClock
from bussdcc.device import DeviceProtocol
from bussdcc.event import EventEngine, EventEngineProtocol
from bussdcc.state import StateEngine, StateEngineProtocol
from bussdcc.service import ServiceProtocol, ServiceSupervisor
from bussdcc.process import ProcessProtocol
from bussdcc.version import get_version

from .protocol import RuntimeProtocol


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

        self.ctx.events.emit("system.booting", version=self.version)

        # Boot all registered devices
        for device in self._devices.values():
            device.attach(self.ctx)

        # Attach processes
        for process in self._processes.values():
            process.attach(self.ctx)

        # Attach interfaces
        for interface in self._interfaces.values():
            interface.attach(self.ctx)

        # Start services under supervisor
        self._service_supervisor = ServiceSupervisor(self.ctx)
        for service in self._services.values():
            self._service_supervisor.register(service)
        self._service_supervisor.start_all()

        self._booted = True
        self.ctx.events.emit("system.booted", version=self.version)

    def shutdown(self, reason: Optional[str] = None) -> None:
        self.ctx.events.emit("system.shutting_down", reason=reason)

        # Stop services first
        if self._service_supervisor:
            self._service_supervisor.stop_all()

        # Detach interfaces
        for interface in self._interfaces.values():
            interface.detach()

        # Detach processes
        for process in self._processes.values():
            process.detach()

        # Detach devices in reverse order
        for device in reversed(list(self._devices.values())):
            device.detach()

        self.ctx.events.emit("system.shutdown")
