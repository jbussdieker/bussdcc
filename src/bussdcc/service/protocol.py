from typing import Protocol

from bussdcc.context import ContextProtocol
from bussdcc.event import Event
from bussdcc.message import Message


class ServiceProtocol(Protocol):
    name: str
    interval: float  # seconds between ticks
    enabled: bool  # start at boot
    restart: bool  # restart if it crashes
    critical: bool  # if True, system may halt on failure

    def attach(self, ctx: ContextProtocol) -> None: ...
    def detach(self) -> None: ...

    def start(self, ctx: ContextProtocol) -> None: ...
    def tick(self, ctx: ContextProtocol) -> None: ...
    def stop(self, ctx: ContextProtocol) -> None: ...

    def handle_event(self, ctx: ContextProtocol, evt: Event[Message]) -> None: ...
