from typing import List, Optional, Type, TypeVar

from bussdcc.context import ContextProtocol
from bussdcc.event import Event
from bussdcc.event.protocol import SubscriptionProtocol
from bussdcc.message import Message

from .protocol import EventSinkProtocol

T = TypeVar("T", bound=Message)


class MemorySink(EventSinkProtocol):
    def __init__(self) -> None:
        self.events: List[Event[Message]] = []
        self._sub: Optional[SubscriptionProtocol] = None

    def start(self, ctx: ContextProtocol) -> None:
        self._sub = ctx.events.subscribe(Message, self.handle)

    def stop(self) -> None:
        if self._sub:
            self._sub.cancel()
            self._sub = None

    def handle(self, evt: Event[Message]) -> None:
        self.events.append(evt)

    def clear(self) -> None:
        self.events.clear()

    def messages(self) -> List[Message]:
        return [e.payload for e in self.events]

    def of_type(self, msg_type: Type[T]) -> List[T]:
        return [
            e.payload
            for e in self.events
            if isinstance(e.payload, msg_type)
        ]

    def last(self) -> Optional[Message]:
        if not self.events:
            return None
        return self.events[-1].payload
