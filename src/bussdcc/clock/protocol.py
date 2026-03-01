from typing import Protocol
from datetime import datetime
import threading


class ClockProtocol(Protocol):
    def sleep(
        self,
        seconds: float,
        cancel: threading.Event | None = None,
    ) -> bool: ...
    def monotonic(self) -> float: ...
    def now_utc(self) -> datetime: ...
