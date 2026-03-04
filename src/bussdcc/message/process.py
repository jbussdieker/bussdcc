from dataclasses import dataclass

from bussdcc.event import Event

from .base import Message
from .severity import Severity


@dataclass(slots=True, frozen=True)
class ProcessStarted(Message):
    process: str


@dataclass(slots=True, frozen=True)
class ProcessStopped(Message):
    process: str


@dataclass(slots=True, frozen=True)
class ProcessError(Message):
    severity = Severity.ERROR

    process: str
    error: str
    evt: Event[Message] | None = None
    traceback: str | None = None
