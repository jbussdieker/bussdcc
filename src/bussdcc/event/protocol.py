from typing import Protocol, Callable, TypeVar

from .event import Event
from ..message import Message

T = TypeVar("T")

EventHandler = Callable[[Event[T]], None]


class SubscriptionProtocol(Protocol):
    def cancel(self) -> None: ...


class EventBusProtocol(Protocol):
    def emit(self, event: Event[Message]) -> None: ...
    def subscribe(
        self, event_type: type[T], handler: EventHandler[T]
    ) -> SubscriptionProtocol: ...
    def unsubscribe(self, subscription: SubscriptionProtocol) -> None: ...
