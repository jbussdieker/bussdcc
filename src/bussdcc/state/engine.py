import threading
from typing import Any

from .protocol import StateEngineProtocol


class StateEngine(StateEngineProtocol):
    """
    Thread-safe hierarchical state storage.

    Supports dot-separated paths:
        se = StateEngine()
        se.set("system.clock.uptime", 42)
        se.get("system.clock.uptime") -> 42
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._state: dict[str, Any] = {}

    def set(self, path: str, value: Any) -> None:
        with self._lock:
            keys = path.split(".")
            d = self._state
            for k in keys[:-1]:
                d = d.setdefault(k, {})
            d[keys[-1]] = value

    def get(self, path: str, default: Any = None) -> Any:
        with self._lock:
            keys = path.split(".")
            d = self._state
            for k in keys:
                if not isinstance(d, dict) or k not in d:
                    return default
                d = d[k]
            return d
