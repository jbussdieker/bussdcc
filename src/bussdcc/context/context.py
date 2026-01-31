from typing import Any, Callable

from bussdcc.clock import Clock
from bussdcc.runtime.protocol import RuntimeProtocol
from bussdcc.event.protocol import EventEngineProtocol
from bussdcc.event.engine import EventEngine, Subscription
from bussdcc.state.protocol import StateEngineProtocol

from .protocol import ContextProtocol


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
