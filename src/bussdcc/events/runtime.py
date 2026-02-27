from dataclasses import dataclass
from typing import Optional

from .base import EventSchema


@dataclass(slots=True)
class RuntimeBooting(EventSchema):
    event = "runtime.booting"

    version: str


@dataclass(slots=True)
class RuntimeBooted(EventSchema):
    event = "runtime.booted"

    version: str


@dataclass(slots=True)
class RuntimeShuttingDown(EventSchema):
    event = "runtime.shutting_down"

    reason: str | None


@dataclass(slots=True)
class RuntimeShutdown(EventSchema):
    event = "runtime.shutdown"

    version: str


@dataclass(slots=True)
class RuntimeSinkFailure(EventSchema):
    event = "runtime.sink.failure"

    sink: str
    error: str
