from typing import Optional
from datetime import datetime

from bussdcc.context import Context, ContextProtocol
from bussdcc.clock import ClockProtocol, ReplayClock
from bussdcc.event import EventBusProtocol
from bussdcc.state import StateStoreProtocol
from bussdcc.io import EventSourceProtocol

from .runtime import Runtime


class ReplayRuntime(Runtime):
    def __init__(
        self,
        *,
        clock: Optional[ClockProtocol] = None,
        events: Optional[EventBusProtocol] = None,
        state: Optional[StateStoreProtocol] = None,
        speed: float = 1.0,
        start_at: Optional[datetime] = None,
    ):
        replay_clock = clock or ReplayClock(speed=speed)
        if not isinstance(replay_clock, ReplayClock):
            raise TypeError("ReplayRuntime requires ReplayClock")

        self._replay_clock = replay_clock
        self.speed = speed
        self.start_at = start_at
        super().__init__(clock=replay_clock, events=events, state=state)

    def replay(self, source: EventSourceProtocol) -> None:
        it = iter(source)

        try:
            first = next(it)
        except StopIteration:
            return

        start_time = self.start_at or first.time

        self._replay_clock.start(start_time)
        self.boot()

        # advance to first event if needed
        if first.time > start_time:
            self._replay_clock.advance_to(first.time)

        self.events.emit(first)

        for evt in it:
            if not self.booted:
                break
            if hasattr(self._replay_clock, "advance_to"):
                self._replay_clock.advance_to(evt.time)
            self.events.emit(evt)

        self._replay_clock.stop()

        self.shutdown("Replay Complete")
