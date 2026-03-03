from dataclasses import dataclass
from typing import Any

from bussdcc.event import Event

from .base import Message
from .level import EventLevel


@dataclass(slots=True, frozen=True)
class DeviceAttached(Message):
    name = "device.attached"

    device: str
    kind: str


@dataclass(slots=True, frozen=True)
class DeviceDetached(Message):
    name = "device.detached"

    device: str
    kind: str


@dataclass(slots=True, frozen=True)
class DeviceFailed(Message):
    name = "device.failed"
    level = EventLevel.ERROR

    device: str
    kind: str
    error: str
    traceback: str | None = None
