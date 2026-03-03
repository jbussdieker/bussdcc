import traceback
from typing import Optional, Dict, Self, Type, Literal, TypeVar
from types import TracebackType

from bussdcc.context import Context, ContextProtocol
from bussdcc.clock import ClockProtocol, SystemClock
from bussdcc.device import DeviceProtocol
from bussdcc.event import Event, EventBus, EventBusProtocol
from bussdcc.message import Message
from bussdcc.state import StateStore, StateStoreProtocol
from bussdcc.service import ServiceProtocol, ServiceSupervisor
from bussdcc.process import ProcessProtocol
from bussdcc.version import get_version

from bussdcc import message

from .protocol import RuntimeProtocol


class Runtime(RuntimeProtocol):
    def __init__(
        self,
        *,
        clock: Optional[ClockProtocol] = None,
        events: EventBusProtocol | None = None,
        state: StateStoreProtocol | None = None,
    ):
        self.clock: ClockProtocol = clock or SystemClock()
        self.events: EventBusProtocol = events or EventBus()
        self.state: StateStoreProtocol = state or StateStore()
        self.version: str = get_version()
        self.ctx: ContextProtocol = Context(
            clock=self.clock, runtime=self, events=self.events, state=self.state
        )

        self._booted: bool = False
        self._devices: Dict[str, DeviceProtocol] = {}
        self._services: Dict[str, ServiceProtocol] = {}
        self._processes: Dict[str, ProcessProtocol] = {}
        self._interfaces: Dict[str, ProcessProtocol] = {}
        self._service_supervisor: ServiceSupervisor | None = None

    def _on_boot(self) -> None:
        """Hook for subclasses to initialize resources."""
        return None

    def _on_shutdown(self, reason: Optional[str] = None) -> None:
        """Hook for subclasses to release resources."""
        return None

    def _dispatch(self, evt: Event[Message]) -> None:
        pass

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

    def register_service(self, service: ServiceProtocol) -> None:
        if self._booted:
            raise RuntimeError("Cannot register services after boot")
        if service.name in self._services:
            raise ValueError(f"Service with name `{service.name}` already registered")
        self._services[service.name] = service

    def register_process(self, process: ProcessProtocol) -> None:
        if self._booted:
            raise RuntimeError("Cannot register processes after boot")
        if process.name in self._processes:
            raise ValueError(f"Process with name `{process.name}` already registered")
        self._processes[process.name] = process

    def register_interface(self, interface: ProcessProtocol) -> None:
        if self._booted:
            raise RuntimeError("Cannot register interfaces after boot")
        if interface.name in self._interfaces:
            raise ValueError(
                f"Interface with name `{interface.name}` already registered"
            )
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

        self._sub = self.events.subscribe(Message, self._dispatch)

        self.ctx.emit(message.RuntimeBooting(version=self.version))

        self._on_boot()

        # Boot all registered devices
        for device in self._devices.values():
            device.attach(self.ctx)

        # Attach processes
        for process in self._processes.values():
            process.attach(self.ctx)
            process.start(self.ctx)
            self.ctx.emit(message.ProcessStarted(process=process.name))

        # Attach interfaces
        for interface in self._interfaces.values():
            interface.attach(self.ctx)
            interface.start(self.ctx)
            self.ctx.emit(message.InterfaceStarted(interface=interface.name))

        self._booted = True
        self.ctx.emit(message.RuntimeBooted(version=self.version))

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
            self.ctx.emit(message.RuntimeShuttingDown(reason=reason))

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
                    self.ctx.emit(message.InterfaceStopped(interface=interface.name))

            # Stop and detach processes
            for process in self._processes.values():
                try:
                    process.stop(self.ctx)
                finally:
                    process.detach()
                    self.ctx.emit(message.ProcessStopped(process=process.name))

            # Detach devices in reverse order
            for device in reversed(list(self._devices.values())):
                device.detach()

            self._on_shutdown(reason)

            self.ctx.emit(message.RuntimeShutdown(version=self.version))

            self._sub.cancel()
        finally:
            # Ensure state is reset even if on_shutdown fails
            self._booted = False
