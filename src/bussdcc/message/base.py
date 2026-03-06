from dataclasses import asdict, dataclass
from typing import ClassVar, Any

from .severity import Severity


@dataclass(slots=True, frozen=True)
class Message:
    severity: ClassVar[Severity] = Severity.INFO
    _registry: ClassVar[dict[str, type["Message"]]] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

        name = cls.__name__
        existing = cls._registry.get(name)

        if existing is None:
            cls._registry[name] = cls
            return

        if existing.__module__ == cls.__module__:
            cls._registry[name] = cls
            return

        raise RuntimeError(
            f"Duplicate message definition for {name}: " f"{existing} vs {cls}"
        )

    @classmethod
    def resolve(cls, key: str) -> type["Message"]:
        try:
            return cls._registry[key]
        except KeyError:
            raise KeyError(f"Unknown message type: {key}") from None

    @classmethod
    def key(cls) -> str:
        return cls.__name__

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
