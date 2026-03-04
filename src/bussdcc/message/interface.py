from dataclasses import dataclass

from bussdcc.event import Event

from .base import Message
from .severity import Severity


@dataclass(slots=True, frozen=True)
class InterfaceStarted(Message):
    interface: str


@dataclass(slots=True, frozen=True)
class InterfaceStopped(Message):
    interface: str
