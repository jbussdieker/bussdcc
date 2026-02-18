from typing import Protocol, Callable, Any

from .event import Event

EventHandler = Callable[[Event], None]


class SubscriptionProtocol(Protocol):
    def cancel(self) -> None: ...


class EventEngineProtocol(Protocol):
    def emit(self, name: str, **data: Any) -> Event: ...
    def subscribe(self, handler: EventHandler) -> SubscriptionProtocol: ...
    def unsubscribe(self, subscription: SubscriptionProtocol) -> None: ...
