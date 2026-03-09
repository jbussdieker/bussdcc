from typing import Optional
from dataclasses import dataclass

from bussdcc.event import Event

from .base import Message
from .severity import Severity


@dataclass(slots=True, frozen=True)
class ServiceError(Message):
    severity = Severity.ERROR

    service: str
    error: str
    evt: Optional[Event[Message]] = None
    traceback: Optional[str] = None


@dataclass(slots=True, frozen=True)
class ServiceFailure(Message):
    severity = Severity.CRITICAL

    service: str
    error: str
    traceback: Optional[str] = None


@dataclass(slots=True, frozen=True)
class ServiceRestart(Message):
    service: str


@dataclass(slots=True, frozen=True)
class ServiceStopped(Message):
    service: str


@dataclass(slots=True, frozen=True)
class ServiceStarted(Message):
    service: str
