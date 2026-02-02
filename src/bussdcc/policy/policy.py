from bussdcc.event.event import Event
from bussdcc.context import ContextProtocol

from .protocol import PolicyProtocol


class Policy(PolicyProtocol):
    name = "allow_all"

    def evaluate(self, ctx: ContextProtocol, evt: Event | None = None) -> bool:
        return True
