from dataclasses import dataclass
from typing import Any

from bussdcc.event import Event

from .base import Message
from .level import EventLevel


@dataclass(slots=True)
class SystemReload(Message):
    name = "system.reload"


@dataclass(slots=True)
class SystemSignal(Message):
    name = "system.signal"

    signal: int
    action: str


@dataclass(slots=True)
class ProcessStarted(Message):
    name = "process.started"

    process: str


@dataclass(slots=True)
class ProcessStopped(Message):
    name = "process.stopped"

    process: str


@dataclass(slots=True)
class ProcessError(Message):
    name = "process.error"
    level = EventLevel.ERROR

    process: str
    error: str
    evt: Event[Message] | None = None
    traceback: str | None = None


@dataclass(slots=True)
class InterfaceStarted(Message):
    name = "interface.started"

    interface: str


@dataclass(slots=True)
class InterfaceStopped(Message):
    name = "interface.stopped"

    interface: str


@dataclass(slots=True)
class DeviceAttached(Message):
    name = "device.attached"

    device: str
    kind: str


@dataclass(slots=True)
class DeviceDetached(Message):
    name = "device.detached"

    device: str
    kind: str


@dataclass(slots=True)
class DeviceFailed(Message):
    name = "device.failed"
    level = EventLevel.ERROR

    device: str
    kind: str
    error: str
    traceback: str | None = None


@dataclass(slots=True)
class ServiceError(Message):
    name = "service.error"
    level = EventLevel.ERROR

    service: str
    error: str
    evt: Event[Message] | None = None
    traceback: str | None = None


@dataclass(slots=True)
class ServiceFailure(Message):
    name = "service.failure"
    level = EventLevel.CRITICAL

    service: str
    error: str
    traceback: str | None = None


@dataclass(slots=True)
class ServiceRestart(Message):
    name = "service.restart"

    service: str


@dataclass(slots=True)
class ServiceStopped(Message):
    name = "service.stopped"

    service: str


@dataclass(slots=True)
class ServiceStarted(Message):
    name = "service.started"

    service: str


@dataclass(slots=True)
class EventSubscriberError(Message):
    name = "event.subscriber_error"
    level = EventLevel.ERROR

    event: str
    handler: str
    error: str
    traceback: str | None = None
