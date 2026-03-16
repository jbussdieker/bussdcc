from typing import ClassVar
from dataclasses import dataclass

from .severity import Severity


@dataclass(slots=True, frozen=True)
class Message:
    severity: ClassVar[Severity] = Severity.INFO
