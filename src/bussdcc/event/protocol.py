from typing import Protocol, Callable, Any

EventHandler = Callable[..., None]


class EventBusProtocol(Protocol):
    """Protocol for an event bus."""

    def emit(self, event: str, **kwargs: Any) -> None: ...
    def on(self, event: str, handler: EventHandler) -> None: ...
