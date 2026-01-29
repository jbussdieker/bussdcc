from typing import Protocol, Callable, Any

from .event import Event
from .engine import Subscription

EventHandler = Callable[[Event], None]


class EventEngineProtocol(Protocol):
    def emit(self, name: str, **data: Any) -> Event: ...
    def subscribe(self, handler: EventHandler) -> Subscription: ...
