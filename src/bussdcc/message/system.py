from dataclasses import dataclass
from typing import Any

from bussdcc.event import Event

from .base import Message
from .severity import Severity


@dataclass(slots=True, frozen=True)
class SystemReload(Message):
    name = "system.reload"


@dataclass(slots=True, frozen=True)
class SystemSignal(Message):
    name = "system.signal"

    signal: int
    action: str


@dataclass(slots=True, frozen=True)
class EventSubscriberError(Message):
    name = "event.subscriber_error"
    severity = Severity.ERROR

    event: str
    handler: str
    error: str
    traceback: str | None = None
