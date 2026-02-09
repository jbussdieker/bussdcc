from typing import Any
import threading

from bussdcc.clock import Clock

from .event import Event
from .protocol import EventHandler, SubscriptionProtocol, EventEngineProtocol


class Subscription:
    def __init__(self, engine: EventEngineProtocol, fn: EventHandler):
        self._engine = engine
        self._fn = fn
        self._active = True

    def cancel(self) -> None:
        if self._active:
            self._engine.unsubscribe(self._fn)
            self._active = False


class EventEngine:
    def __init__(self, clock: Clock) -> None:
        self.clock = clock
        self._lock = threading.RLock()
        self._subs: list[EventHandler] = []

    def subscribe(self, fn: EventHandler) -> SubscriptionProtocol:
        with self._lock:
            self._subs.append(fn)
        return Subscription(self, fn)

    def unsubscribe(self, fn: EventHandler) -> None:
        with self._lock:
            if fn in self._subs:
                self._subs.remove(fn)

    def emit(self, name: str, **data: Any) -> Event:
        evt = Event(
            time=self.clock.now_utc().isoformat(),
            name=name,
            data=data,
        )

        with self._lock:
            subs = list(self._subs)

        errors = []

        for fn in subs:
            try:
                fn(evt)
            except Exception as e:
                errors.append(
                    {
                        "event": evt.name,
                        "subscriber": repr(fn),
                        "error": repr(e),
                    }
                )

        if name != "event.subscriber_error":
            for error in errors:
                self.emit("event.subscriber_error", **error)

        return evt
