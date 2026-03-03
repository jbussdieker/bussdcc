from bussdcc.event import Event
from bussdcc.context import ContextProtocol
from bussdcc.message import Message

from .protocol import ProcessProtocol


class Process(ProcessProtocol):
    name = "unnamed"

    ctx: ContextProtocol | None

    def attach(self, ctx: ContextProtocol) -> None:
        self.ctx = ctx

    def detach(self) -> None:
        self.ctx = None

    def start(self, ctx: ContextProtocol) -> None:
        pass

    def stop(self, ctx: ContextProtocol) -> None:
        pass

    def handle_event(self, ctx: ContextProtocol, evt: Event[Message]) -> None:
        pass
