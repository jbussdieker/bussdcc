from typing import List, Optional, Type, TypeVar

from bussdcc.runtime import Runtime
from bussdcc.clock import FakeClock
from bussdcc.message import Message
from bussdcc.event import Event
from bussdcc.io.memory_sink import MemorySink

T = TypeVar("T", bound=Message)


class RuntimeHarness:
    def __init__(self, *, fake_time: bool = False):
        self._clock = FakeClock() if fake_time else None
        self.runtime = Runtime(clock=self._clock) if self._clock else Runtime()
        self.sink = MemorySink()

    def boot(self) -> None:
        self.sink.start(self.runtime.ctx)
        self.runtime.boot()

    def shutdown(self) -> None:
        self.runtime.shutdown()
        self.sink.stop()

    def __enter__(self) -> "RuntimeHarness":
        self.boot()
        return self

    def __exit__(self, *_) -> None:
        self.shutdown()

    @property
    def clock(self) -> FakeClock:
        assert isinstance(self.runtime.clock, FakeClock)
        return self.runtime.clock

    @property
    def events(self) -> List[Event[Message]]:
        return self.sink.events

    def messages(self) -> List[Message]:
        return self.sink.messages()

    def of_type(self, msg_type: Type[T]) -> List[T]:
        return self.sink.of_type(msg_type)

    def last(self, msg_type: Type[T]) -> Optional[T]:
        events = self.of_type(msg_type)
        return events[-1] if events else None

    def assert_emitted(self, msg_type: Type[Message]) -> None:
        if not self.of_type(msg_type):
            raise AssertionError(f"{msg_type.__name__} was not emitted")

    def assert_not_emitted(self, msg_type: Type[Message]) -> None:
        if self.of_type(msg_type):
            raise AssertionError(f"{msg_type.__name__} was unexpectedly emitted")

    def clear(self) -> None:
        self.sink.clear()
