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

    def sleep(self, seconds: float) -> None:
        self.clock.sleep(seconds)

    def emit(self, event: str, **kwargs: Any) -> None:
        self.events.emit(event, **kwargs)

    def on(self, handler: Callable[..., None]) -> Subscription:
        return self.events.subscribe(handler)
