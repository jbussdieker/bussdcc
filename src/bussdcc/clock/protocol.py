from typing import Protocol, Optional
from datetime import datetime
import threading


class ClockProtocol(Protocol):
    def sleep(
        self,
        seconds: float,
        cancel: Optional[threading.Event] = None,
    ) -> bool: ...
    def monotonic(self) -> float: ...
    def uptime(self) -> float: ...
    def now_utc(self) -> datetime: ...
