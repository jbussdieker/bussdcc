from dataclasses import dataclass
from typing import Any

from bussdcc.event import Event

from .base import EventSchema
from .level import EventLevel


@dataclass(slots=True)
class SystemReload(EventSchema):
    name = "system.reload"


@dataclass(slots=True)
class SystemSignal(EventSchema):
    name = "system.signal"

    signal: int
    action: str


@dataclass(slots=True)
class ProcessStarted(EventSchema):
    name = "process.started"

    process: str


@dataclass(slots=True)
class ProcessStopped(EventSchema):
    name = "process.stopped"

    process: str


@dataclass(slots=True)
class ProcessError(EventSchema):
    name = "process.error"
    level = EventLevel.ERROR

    process: str
    error: str
    evt: Event[EventSchema] | None = None
    traceback: str | None = None


@dataclass(slots=True)
class InterfaceStarted(EventSchema):
    name = "interface.started"

    interface: str


@dataclass(slots=True)
class InterfaceStopped(EventSchema):
    name = "interface.stopped"

    interface: str


@dataclass(slots=True)
class DeviceAttached(EventSchema):
    name = "device.attached"

    device: str
    kind: str


@dataclass(slots=True)
class DeviceDetached(EventSchema):
    name = "device.detached"

    device: str
    kind: str


@dataclass(slots=True)
class DeviceFailed(EventSchema):
    name = "device.failed"
    level = EventLevel.ERROR

    device: str
    kind: str
    error: str
    traceback: str | None = None


@dataclass(slots=True)
class ServiceError(EventSchema):
    name = "service.error"
    level = EventLevel.ERROR

    service: str
    error: str
    evt: Event[EventSchema] | None = None
    traceback: str | None = None


@dataclass(slots=True)
class ServiceFailure(EventSchema):
    name = "service.failure"
    level = EventLevel.CRITICAL

    service: str
    error: str
    traceback: str | None = None


@dataclass(slots=True)
class ServiceRestart(EventSchema):
    name = "service.restart"

    service: str


@dataclass(slots=True)
class ServiceStopped(EventSchema):
    name = "service.stopped"

    service: str


@dataclass(slots=True)
class ServiceStarted(EventSchema):
    name = "service.started"

    service: str


@dataclass(slots=True)
class EventSubscriberError(EventSchema):
    name = "event.subscriber_error"
    level = EventLevel.ERROR

    event: str
    handler: str
    error: str
    traceback: str | None = None
