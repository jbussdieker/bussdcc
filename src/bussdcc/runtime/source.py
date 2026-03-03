from typing import Protocol, Iterator

from bussdcc.event import Event
from bussdcc.message import Message


class EventSource(Protocol):
    """
    A replayable source of historical events.

    Must yield Event[Message] in chronological order.
    """

    def __iter__(self) -> Iterator[Event[Message]]: ...
