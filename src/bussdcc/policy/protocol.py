from typing import Protocol
from bussdcc.context import ContextProtocol
from bussdcc.event.event import Event


class PolicyProtocol(Protocol):
    name: str

    def evaluate(self, ctx: ContextProtocol, evt: Event | None = None) -> bool: ...
