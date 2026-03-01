from dataclasses import dataclass
from typing import Optional

from .base import Message


@dataclass(slots=True)
class RuntimeBooting(Message):
    name = "runtime.booting"

    version: str


@dataclass(slots=True)
class RuntimeBooted(Message):
    name = "runtime.booted"

    version: str


@dataclass(slots=True)
class RuntimeShuttingDown(Message):
    name = "runtime.shutting_down"

    reason: str | None


@dataclass(slots=True)
class RuntimeShutdown(Message):
    name = "runtime.shutdown"

    version: str
