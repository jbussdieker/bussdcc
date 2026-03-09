from typing import Optional
import time
import threading
from datetime import datetime, timedelta

from bussdcc.clock import ClockProtocol


class ReplayClock(ClockProtocol):
    def __init__(self, *, speed: float = 1.0):
        self.speed = speed
        self._lock = threading.Condition()
        self._now: Optional[datetime] = None
        self._monotonic = 0.0
        self._running = True

    def now_utc(self) -> datetime:
        assert self._now is not None, "Replay clock not started"
        return self._now

    def monotonic(self) -> float:
        return self._monotonic

    def sleep(self, seconds: float, cancel: Optional[threading.Event] = None) -> bool:
        target = self._monotonic + seconds

        with self._lock:
            while self._running and self._monotonic < target:
                if cancel and cancel.is_set():
                    return True
                self._lock.wait()

        return False

    def advance_to(self, new_time: datetime) -> None:
        with self._lock:
            if self._now is None:
                self._now = new_time
                return

            delta = (new_time - self._now).total_seconds()
            if delta > 0 and self.speed > 0:
                time.sleep(delta / self.speed)

            self._now = new_time
            self._monotonic += max(delta, 0)

            self._lock.notify_all()

    def start(self, start_time: datetime) -> None:
        with self._lock:
            if self._now is not None:
                raise RuntimeError("ReplayClock already started")

            self._now = start_time
            self._monotonic = 0.0
            self._lock.notify_all()

    def stop(self) -> None:
        with self._lock:
            self._running = False
            self._lock.notify_all()
