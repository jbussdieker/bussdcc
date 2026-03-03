from dataclasses import dataclass
from typing import Any

from bussdcc.event import Event

from .base import Message
from .severity import Severity


@dataclass(slots=True, frozen=True)
class ServiceError(Message):
    name = "service.error"
    severity = Severity.ERROR

    service: str
    error: str
    evt: Event[Message] | None = None
    traceback: str | None = None


@dataclass(slots=True, frozen=True)
class ServiceFailure(Message):
    name = "service.failure"
    severity = Severity.CRITICAL

    service: str
    error: str
    traceback: str | None = None


@dataclass(slots=True, frozen=True)
class ServiceRestart(Message):
    name = "service.restart"

    service: str


@dataclass(slots=True, frozen=True)
class ServiceStopped(Message):
    name = "service.stopped"

    service: str


@dataclass(slots=True, frozen=True)
class ServiceStarted(Message):
    name = "service.started"

    service: str
