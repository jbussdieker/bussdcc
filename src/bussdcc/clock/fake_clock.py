from datetime import datetime, timedelta, timezone
from typing import Optional
import threading

from .protocol import ClockProtocol


class FakeClock(ClockProtocol):
    def __init__(self, start: Optional[datetime] = None):
        self._lock = threading.Condition()
        self._now = start or datetime(2000, 1, 1, tzinfo=timezone.utc)
        self._monotonic = 0.0
        self._running = True

    def now_utc(self) -> datetime:
        return self._now

    def monotonic(self) -> float:
        return self._monotonic

    def sleep(
        self,
        seconds: float,
        cancel: Optional[threading.Event] = None,
    ) -> bool:
        target = self._monotonic + seconds

        with self._lock:
            while self._running and self._monotonic < target:
                if cancel and cancel.is_set():
                    return True
                self._lock.wait()

        return False

    def advance(self, seconds: float) -> None:
        with self._lock:
            self._monotonic += seconds
            self._now += timedelta(seconds=seconds)
            self._lock.notify_all()

    def set(self, new_time: datetime) -> None:
        with self._lock:
            delta = (new_time - self._now).total_seconds()
            self._monotonic += max(delta, 0)
            self._now = new_time
            self._lock.notify_all()

    def stop(self) -> None:
        with self._lock:
            self._running = False
            self._lock.notify_all()
