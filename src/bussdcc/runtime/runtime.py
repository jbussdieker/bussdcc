import traceback
from typing import Optional, Dict, Self, Type, Literal, TypeVar
from types import TracebackType

from bussdcc.context import Context, ContextProtocol
from bussdcc.clock import ClockProtocol, SystemClock
from bussdcc.device import DeviceProtocol, DeviceManager
from bussdcc.event import Event, EventBus, EventBusProtocol
from bussdcc.message import Message, Severity
from bussdcc.state import StateStore, StateStoreProtocol
from bussdcc.service import ServiceProtocol, ServiceSupervisor
from bussdcc.process import ProcessProtocol, ProcessManager
from bussdcc.interface import InterfaceManager
from bussdcc.version import get_version

from bussdcc import message

from .protocol import RuntimeProtocol


class Runtime(RuntimeProtocol):
    def __init__(
        self,
        *,
        clock: Optional[ClockProtocol] = None,
        events: Optional[EventBusProtocol] = None,
        state: Optional[StateStoreProtocol] = None,
    ):
        self.clock: ClockProtocol = clock or SystemClock()
        self.events: EventBusProtocol = events or EventBus()
        self.state: StateStoreProtocol = state or StateStore()
        self.version: str = get_version()
        self.ctx: ContextProtocol = Context(
            clock=self.clock, runtime=self, events=self.events, state=self.state
        )

        self._booted: bool = False
        self.interfaces = InterfaceManager(self.ctx)
        self.processes = ProcessManager(self.ctx)
        self.devices = DeviceManager(self.ctx)
        self.services = ServiceSupervisor(self.ctx)

    def _on_boot(self) -> None:
        """Hook for subclasses to initialize resources."""
        return None

    def _on_shutdown(self, reason: Optional[str] = None) -> None:
        """Hook for subclasses to release resources."""
        return None

    def _dispatch_to_process(
        self, process: ProcessProtocol, evt: Event[Message]
    ) -> None:
        try:
            process.handle_event(self.ctx, evt)
        except Exception as e:
            if evt.payload.severity >= Severity.ERROR:
                return

            self.ctx.emit(
                message.ProcessError(
                    process=process.name,
                    error=repr(e),
                    evt=evt,
                    traceback=traceback.format_exc(),
                )
            )

    def _dispatch_to_service(
        self, service: ServiceProtocol, evt: Event[Message]
    ) -> None:
        try:
            service.handle_event(self.ctx, evt)
        except Exception as e:
            if evt.payload.severity >= Severity.ERROR:
                return

            self.ctx.emit(
                message.ServiceError(
                    service=service.name,
                    error=repr(e),
                    evt=evt,
                    traceback=traceback.format_exc(),
                )
            )

    def _dispatch(self, evt: Event[Message]) -> None:
        """
        Authoritative dispatch entrypoint.

        Called for every emitted Message.
        """

        # Processes
        for process in self.processes.list():
            self._dispatch_to_process(process, evt)

        # Interfaces
        for interface in self.interfaces.list():
            self._dispatch_to_process(interface, evt)

        # Services (event-driven side)
        for service in self.services.running():
            self._dispatch_to_service(service, evt)

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

    def boot(self) -> None:
        if self._booted:
            return

        # Runtime is the authoritative dispatcher for all messages
        self._sub = self.events.subscribe(Message, self._dispatch)

        self.ctx.emit(message.RuntimeBooting(version=self.version))
        self._on_boot()
        self.devices.boot()
        self.processes.boot()
        self.interfaces.boot()
        self._booted = True
        self.ctx.emit(message.RuntimeBooted(version=self.version))
        self.services.boot()

    def shutdown(self, reason: Optional[str] = None) -> None:
        if not self._booted:
            return  # Be idempotent on shutdown to avoid exit crashes

        try:
            self.ctx.emit(message.RuntimeShuttingDown(reason=reason))
            self.services.shutdown()
            self.interfaces.shutdown()
            self.processes.shutdown()
            self.devices.shutdown()
            self._on_shutdown(reason)
            self.ctx.emit(message.RuntimeShutdown(version=self.version))
            self._sub.cancel()
        finally:
            # Ensure state is reset even if on_shutdown fails
            self._booted = False
