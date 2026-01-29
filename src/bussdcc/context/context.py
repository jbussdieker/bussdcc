from typing import Any, Callable

from bussdcc.clock import Clock
from bussdcc.runtime.protocol import RuntimeProtocol
from bussdcc.event.protocol import EventBusProtocol
from bussdcc.event.bus import EventBus

from .protocol import ContextProtocol


class Context(ContextProtocol):
    def __init__(
        self,
        clock: Clock,
        runtime: RuntimeProtocol,
        event_bus: EventBusProtocol | None = None,
    ):
        self.clock: Clock = clock
        self.runtime: RuntimeProtocol = runtime
        self.events: EventBusProtocol = event_bus or EventBus()

    def sleep(self, seconds: float) -> None:
        self.clock.sleep(seconds)

    def emit(self, event: str, **kwargs: Any) -> None:
        self.events.emit(event, **kwargs)

    def on(self, event: str, handler: Callable[..., None]) -> None:
        self.events.on(event, handler)
