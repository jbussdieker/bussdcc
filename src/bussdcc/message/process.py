from dataclasses import dataclass

from bussdcc.event import Event

from .base import Message
from .severity import Severity


@dataclass(slots=True, frozen=True)
class ProcessStarted(Message):
    name = "process.started"

    process: str


@dataclass(slots=True, frozen=True)
class ProcessStopped(Message):
    name = "process.stopped"

    process: str


@dataclass(slots=True, frozen=True)
class ProcessError(Message):
    name = "process.error"
    severity = Severity.ERROR

    process: str
    error: str
    evt: Event[Message] | None = None
    traceback: str | None = None
