from dataclasses import dataclass
from typing import Any

from bussdcc.event import Event

from .base import Message
from .severity import Severity


@dataclass(slots=True, frozen=True)
class InterfaceStarted(Message):
    name = "interface.started"

    interface: str


@dataclass(slots=True, frozen=True)
class InterfaceStopped(Message):
    name = "interface.stopped"

    interface: str
