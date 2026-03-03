from dataclasses import asdict, dataclass
from typing import ClassVar, Any

from .severity import Severity


@dataclass(slots=True, frozen=True)
class Message:
    name: ClassVar[str]
    severity: ClassVar[Severity] = Severity.INFO

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
