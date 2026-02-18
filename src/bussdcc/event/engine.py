from typing import List, Any
import threading

from bussdcc.clock import Clock

from .event import Event
from .protocol import EventHandler, SubscriptionProtocol, EventEngineProtocol


class _Subscription:
    def __init__(self, engine: EventEngine, handler: EventHandler):
        self._engine = engine
        self._handler = handler
        self._cancelled = False

    def cancel(self) -> None:
        if not self._cancelled:
            self._engine._unsubscribe(self)
            self._cancelled = True

    @property
    def handler(self) -> EventHandler:
        return self._handler


class EventEngine:
    def __init__(self, clock: Clock) -> None:
        self.clock = clock
        self._lock = threading.RLock()
        self._subscriptions: List[_Subscription] = []

    def subscribe(self, handler: EventHandler) -> SubscriptionProtocol:
        sub = _Subscription(self, handler)
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

    def emit(self, name: str, **data: Any) -> Event:
        evt = Event(
            time=self.clock.now_utc(),
            name=name,
            data=data,
        )

        with self._lock:
            subs = list(self._subscriptions)

        errors = []

        for sub in subs:
            try:
                sub.handler(evt)
            except Exception as e:
                errors.append(
                    {
                        "event": evt.name,
                        "subscriber": repr(sub.handler),
                        "error": repr(e),
                    }
                )

        if name != "event.subscriber_error":
            for error in errors:
                self.emit("event.subscriber_error", **error)

        return evt
