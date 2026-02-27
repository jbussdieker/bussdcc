from dataclasses import dataclass
from typing import Optional

from .base import EventSchema


@dataclass(slots=True)
class RuntimeBooting(EventSchema):
    name = "runtime.booting"

    version: str


@dataclass(slots=True)
class RuntimeBooted(EventSchema):
    name = "runtime.booted"

    version: str


@dataclass(slots=True)
class RuntimeShuttingDown(EventSchema):
    name = "runtime.shutting_down"

    reason: str | None


@dataclass(slots=True)
class RuntimeShutdown(EventSchema):
    name = "runtime.shutdown"

    version: str
