from typing import Callable, Deque, Any
from collections import deque
from dataclasses import dataclass
import threading

from bussdcc.clock import Clock

from .event import Event


class Subscription:
    def __init__(self, engine: "EventEngine", fn: Callable[[Event], None]):
        self._engine = engine
        self._fn = fn
        self._active = True

    def cancel(self) -> None:
        if self._active:
            self._engine._unsubscribe(self._fn)
            self._active = False


class EventEngine:
    def __init__(self, clock: Clock, max_events: int = 1000) -> None:
        self.clock = clock
        self._lock = threading.RLock()
        self._events: Deque[Event] = deque(maxlen=max_events)
        self._subs: list[Callable[[Event], None]] = []

    def subscribe(self, fn: Callable[[Event], None]) -> Subscription:
        with self._lock:
            self._subs.append(fn)
        return Subscription(self, fn)

    def _unsubscribe(self, fn: Callable[[Event], None]) -> None:
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
            self._events.appendleft(evt)
            subs = list(self._subs)

        for fn in subs:
            try:
                fn(evt)
            except Exception as e:
                err_evt = Event(
                    time=self.clock.now_utc().isoformat(),
                    name="event.subscriber_error",
                    data={"error": repr(e)},
                )
                with self._lock:
                    self._events.appendleft(err_evt)

        return evt

    def recent(self, n: int = 10) -> list[Event]:
        with self._lock:
            return list(self._events)[:n]
