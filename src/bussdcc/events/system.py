from dataclasses import dataclass
from typing import Any

from bussdcc.event import Event

from .base import EventSchema


@dataclass(slots=True)
class SystemReload(EventSchema):
    event = "system.reload"


@dataclass(slots=True)
class SystemSignal(EventSchema):
    event = "system.signal"

    signal: int
    action: str


@dataclass(slots=True)
class ProcessStarted(EventSchema):
    event = "process.started"

    process: str


@dataclass(slots=True)
class ProcessStopped(EventSchema):
    event = "process.stopped"

    process: str


@dataclass(slots=True)
class ProcessError(EventSchema):
    event = "process.error"

    process: str
    error: str
    evt: Event[object] | None = None
    traceback: str | None = None


@dataclass(slots=True)
class InterfaceStarted(EventSchema):
    event = "interface.started"

    interface: str


@dataclass(slots=True)
class InterfaceStopped(EventSchema):
    event = "interface.stopped"

    interface: str


@dataclass(slots=True)
class DeviceAttached(EventSchema):
    event = "device.attached"

    device: str
    kind: str


@dataclass(slots=True)
class DeviceDetached(EventSchema):
    event = "device.detached"

    device: str
    kind: str


@dataclass(slots=True)
class DeviceFailed(EventSchema):
    event = "device.failed"

    device: str
    kind: str
    error: str
    traceback: str | None = None


@dataclass(slots=True)
class ServiceError(EventSchema):
    event = "service.error"

    service: str
    error: str
    evt: Event[object] | None = None
    traceback: str | None = None


@dataclass(slots=True)
class ServiceFailure(EventSchema):
    event = "service.failure"

    service: str
    error: str
    traceback: str | None = None


@dataclass(slots=True)
class ServiceRestart(EventSchema):
    event = "service.restart"

    service: str


@dataclass(slots=True)
class ServiceStopped(EventSchema):
    event = "service.stopped"

    service: str


@dataclass(slots=True)
class ServiceStarted(EventSchema):
    event = "service.started"

    service: str
