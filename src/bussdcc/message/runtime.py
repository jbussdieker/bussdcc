from dataclasses import dataclass
from typing import Optional

from .base import Message


@dataclass(slots=True, frozen=True)
class RuntimeBooting(Message):
    version: str


@dataclass(slots=True, frozen=True)
class RuntimeBooted(Message):
    version: str


@dataclass(slots=True, frozen=True)
class RuntimeShuttingDown(Message):
    reason: str | None


@dataclass(slots=True, frozen=True)
class RuntimeShutdown(Message):
    version: str
