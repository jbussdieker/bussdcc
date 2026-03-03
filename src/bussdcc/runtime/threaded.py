import threading
from typing import Optional

from bussdcc.clock import ClockProtocol
from bussdcc.event import EventBusProtocol
from bussdcc.state import StateStoreProtocol

from .runtime import Runtime


class ThreadedRuntime(Runtime):
    """
    Runtime variant that owns a background execution thread.

    - boot() and shutdown() remain synchronous
    - run() blocks the caller until shutdown
    """

    def __init__(
        self,
        *,
        clock: Optional[ClockProtocol] = None,
        events: Optional[EventBusProtocol] = None,
        state: Optional[StateStoreProtocol] = None,
    ):
        super().__init__(clock=clock, events=events, state=state)
        self._stop_event = threading.Event()

    def run(self) -> None:
        self._stop_event.clear()

        with self:
            self._stop_event.wait()

    def shutdown(self, reason: Optional[str] = None) -> None:
        if not self.booted:
            return

        try:
            super().shutdown(reason=reason)
        finally:
            self._stop_event.set()
