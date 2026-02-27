from typing import TypeVar

from bussdcc.clock import Clock
from bussdcc.event import Event
from bussdcc.events import EventSchema
from bussdcc.runtime.protocol import RuntimeProtocol
from bussdcc.event.protocol import EventEngineProtocol
from bussdcc.state.protocol import StateEngineProtocol

from .protocol import ContextProtocol

T = TypeVar("T")


class Context(ContextProtocol):
    def __init__(
        self,
        clock: Clock,
        runtime: RuntimeProtocol,
        events: EventEngineProtocol,
        state: StateEngineProtocol,
    ):
        self.clock: Clock = clock
        self.runtime: RuntimeProtocol = runtime
        self.events = events
        self.state = state

    def emit(self, payload: EventSchema) -> None:
        self.events.emit(Event(time=self.clock.now_utc(), payload=payload))
