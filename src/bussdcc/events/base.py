from dataclasses import asdict, dataclass
from typing import ClassVar, Any


@dataclass(slots=True)
class EventSchema:
    event: ClassVar[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
