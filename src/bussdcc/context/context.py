from typing import TypeVar

from bussdcc.clock import ClockProtocol
from bussdcc.event import Event
from bussdcc.message import Message
from bussdcc.runtime.protocol import RuntimeProtocol
from bussdcc.event.protocol import EventBusProtocol
from bussdcc.state.protocol import StateStoreProtocol

from .protocol import ContextProtocol

T = TypeVar("T")


class Context(ContextProtocol):
    def __init__(
        self,
        clock: ClockProtocol,
        runtime: RuntimeProtocol,
        events: EventBusProtocol,
        state: StateStoreProtocol,
    ):
        self.clock: ClockProtocol = clock
        self.runtime: RuntimeProtocol = runtime
        self.events = events
        self.state = state

    def emit(self, message: Message) -> None:
        self.events.emit(Event(time=self.clock.now_utc(), payload=message))
