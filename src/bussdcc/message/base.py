from dataclasses import asdict, dataclass
from typing import ClassVar, Any

from .level import EventLevel


@dataclass(slots=True)
class Message:
    name: ClassVar[str]
    level: ClassVar[EventLevel] = EventLevel.INFO

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
