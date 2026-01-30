from typing import Protocol
from bussdcc.context import ContextProtocol


class ServiceProtocol(Protocol):
    name: str

    def start(self, ctx: ContextProtocol) -> None: ...
    def tick(self, ctx: ContextProtocol) -> None: ...
    def stop(self, ctx: ContextProtocol) -> None: ...
