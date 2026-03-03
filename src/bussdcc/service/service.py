from bussdcc.event import Event
from bussdcc.context import ContextProtocol
from bussdcc.message import Message

from .protocol import ServiceProtocol


class Service(ServiceProtocol):
    name = "unnamed"

    # execution model
    interval = 1.0  # seconds between ticks
    enabled = True  # start at boot
    restart = True  # restart if it crashes
    critical = False  # if True, system may halt on failure

    ctx: ContextProtocol | None

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
