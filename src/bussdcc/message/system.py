from typing import Optional
from dataclasses import dataclass

from bussdcc.event import Event

from .base import Message
from .severity import Severity


@dataclass(slots=True, frozen=True)
class SystemReload(Message):
    pass


@dataclass(slots=True, frozen=True)
class SystemSignal(Message):
    signal: int
    action: str


@dataclass(slots=True, frozen=True)
class EventSubscriberError(Message):
    severity = Severity.ERROR

    event: Event[Message]
    handler: str
    error: str
    traceback: Optional[str] = None
