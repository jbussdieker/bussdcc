from typing import List, Any, TypeVar
import threading

from bussdcc.clock import Clock

from .event import Event
from .handler import TypedHandler
from .protocol import EventHandler, SubscriptionProtocol, EventEngineProtocol

T = TypeVar("T")


class _Subscription:
    def __init__(self, engine: "EventEngine", handler: TypedHandler[T]):
        self._engine = engine
        self._handler = handler
        self._cancelled = False

    def cancel(self) -> None:
        if not self._cancelled:
            self._engine._unsubscribe(self)
            self._cancelled = True


class EventEngine(EventEngineProtocol):
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._subscriptions: List[_Subscription] = []

    def subscribe(
        self, event_type: type[T], handler: EventHandler[T]
    ) -> SubscriptionProtocol:
        wrapped = TypedHandler(event_type, handler)
        sub = _Subscription(self, wrapped)
        with self._lock:
            self._subscriptions.append(sub)
        return sub

    def _unsubscribe(self, subscription: _Subscription) -> None:
        with self._lock:
            try:
                self._subscriptions.remove(subscription)
            except ValueError:
                pass

    def unsubscribe(self, subscription: SubscriptionProtocol) -> None:
        subscription.cancel()

    def emit(self, evt: Event[object]) -> None:
        with self._lock:
            subs = list(self._subscriptions)

        # errors = []

        for sub in subs:
            try:
                sub._handler.handle(evt)
            except Exception as e:
                pass
                # errors.append(
                #    {
                #        "event": evt.name,
                #        "subscriber": repr(sub.handler),
                #        "error": repr(e),
                #    }
                # )

        # if event_name != "event.subscriber_error":
        #    for error in errors:
        #        self.emit("event.subscriber_error", **error)
