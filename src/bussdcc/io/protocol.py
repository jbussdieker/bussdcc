from typing import Protocol, Iterator

from bussdcc.context.protocol import ContextProtocol
from bussdcc.event import Event
from bussdcc.message import Message


class EventSourceProtocol(Protocol):
    def __iter__(self) -> Iterator[Event[Message]]: ...


class EventSinkProtocol(Protocol):
    def start(self, ctx: ContextProtocol) -> None: ...
    def stop(self) -> None: ...
    def handle(self, evt: Event[Message]) -> None: ...
