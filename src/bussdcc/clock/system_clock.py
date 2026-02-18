import threading
from datetime import datetime, timezone
import time

from .protocol import Clock


class SystemClock(Clock):
    def __init__(self) -> None:
        self._origin = time.monotonic()

    def now_utc(self) -> datetime:
        return datetime.now(timezone.utc)

    def monotonic(self) -> float:
        return time.monotonic()

    def uptime(self) -> float:
        return time.monotonic() - self._origin

    def sleep(
        self,
        seconds: float,
        cancel: threading.Event | None = None,
    ) -> bool:
        if cancel is None:
            time.sleep(seconds)
            return False

        deadline = self.monotonic() + seconds

        while True:
            remaining = deadline - self.monotonic()
            if remaining <= 0:
                return False  # normal wake

            # wait at most 0.5s so cancellation is responsive
            if cancel.wait(min(remaining, 0.5)):
                return True  # interrupted
