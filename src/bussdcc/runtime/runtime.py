from typing import Optional, Dict

from bussdcc.context import Context, ContextProtocol
from bussdcc.clock import Clock, SystemClock
from bussdcc.device import DeviceProtocol
from bussdcc.event import EventEngine
from bussdcc.state import StateEngine
from bussdcc.service import ServiceProtocol, ServiceSupervisor
from bussdcc.process import ProcessProtocol
from bussdcc.version import get_version

from .protocol import RuntimeProtocol


class Runtime(RuntimeProtocol):
    def __init__(self, *, clock: Optional[Clock] = None):
        self.clock: Clock = clock or SystemClock()
        self.events = EventEngine(clock=self.clock)
        self.state = StateEngine()
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

    def register_device(self, device: DeviceProtocol) -> None:
        if self._booted:
            raise RuntimeError("Cannot register devices after boot")
        self._devices[device.name] = device

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

    def get_device(self, name: str) -> DeviceProtocol | None:
        """Retrieve a registered device by name."""
        return self._devices.get(name)

    def list_devices(self) -> list[str]:
        """Return a list of registered device names."""
        return list(self._devices.keys())

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
