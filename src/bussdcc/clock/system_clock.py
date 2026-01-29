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

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)
