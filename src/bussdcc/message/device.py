from dataclasses import dataclass

from bussdcc.event import Event

from .base import Message
from .severity import Severity


@dataclass(slots=True, frozen=True)
class DeviceAttached(Message):
    device: str
    kind: str


@dataclass(slots=True, frozen=True)
class DeviceDetached(Message):
    device: str
    kind: str


@dataclass(slots=True, frozen=True)
class DeviceFailed(Message):
    severity = Severity.ERROR

    device: str
    kind: str
    error: str
    traceback: str | None = None
