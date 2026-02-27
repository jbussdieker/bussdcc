from typing import Protocol, Callable, Any, TypeVar

from .event import Event

T = TypeVar("T")

EventHandler = Callable[[Event[T]], None]


class SubscriptionProtocol(Protocol):
    def cancel(self) -> None: ...


class EventEngineProtocol(Protocol):
    def emit(self, event: Event[object]) -> None: ...
    def subscribe(
        self, event_type: type[T], handler: EventHandler[T]
    ) -> SubscriptionProtocol: ...
    def unsubscribe(self, subscription: SubscriptionProtocol) -> None: ...
