from dataclasses import asdict, dataclass
from typing import ClassVar, Any

from .severity import Severity


@dataclass(slots=True, frozen=True)
class Message:
    severity: ClassVar[Severity] = Severity.INFO
    _registry: ClassVar[dict[str, type["Message"]]] = {}

    def __init_subclass__(cls) -> None:
        key = f"{cls.__module__}.{cls.__qualname__}"
        Message._registry[key] = cls

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def resolve(cls, key: str) -> type["Message"]:
        return cls._registry[key]

    @classmethod
    def key_for(cls, message: "Message") -> str:
        c = type(message)
        return f"{c.__module__}.{c.__qualname__}"
