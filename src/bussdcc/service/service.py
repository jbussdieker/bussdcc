from bussdcc.event import Event
from bussdcc.context import ContextProtocol
from bussdcc.message import Message

from .protocol import ServiceProtocol


class Service(ServiceProtocol):
    name = "unnamed"

    interval = 1.0
    enabled = True
    restart = True
    critical = False

    ctx: ContextProtocol | None = None

    def attach(self, ctx: ContextProtocol) -> None:
        self.ctx = ctx

    def detach(self) -> None:
        self.ctx = None

    def start(self, ctx: ContextProtocol) -> None:
        """Called once when the service starts"""
        pass

    def tick(self, ctx: ContextProtocol) -> None:
        """Called repeatedly while the service is running"""
        pass

    def stop(self, ctx: ContextProtocol) -> None:
        """Called once when the service is stopping"""
        pass

    def handle_event(self, ctx: ContextProtocol, evt: Event[Message]) -> None:
        pass
