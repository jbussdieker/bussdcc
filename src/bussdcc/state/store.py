from typing import Any, Callable
import threading

from .protocol import StateStoreProtocol
from .path import parse_path


class StateStore(StateStoreProtocol):
    """
    Thread-safe hierarchical state storage.

    Supports dot-separated paths:
        se = StateStore()
        se.set("system.clock.uptime", 42)
        se.get("system.clock.uptime") -> 42
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._state: dict[str, Any] = {}

    def set(self, path: str, value: Any) -> None:
        with self._lock:
            keys = parse_path(path)
            d = self._state
            for k in keys[:-1]:
                nxt = d.setdefault(k, {})
                if not isinstance(nxt, dict):
                    raise TypeError(f"Path conflict at '{k}'")
                d = nxt
            d[keys[-1]] = value

    def get(self, path: str, default: Any = None) -> Any:
        with self._lock:
            keys = parse_path(path)
            d = self._state
            for k in keys:
                if not isinstance(d, dict) or k not in d:
                    return default
                d = d[k]
            return d

    def update(self, path: str, fn: Callable[[Any], Any]) -> Any:
        with self._lock:
            keys = parse_path(path)
            d = self._state

            for k in keys[:-1]:
                nxt = d.setdefault(k, {})
                if not isinstance(nxt, dict):
                    raise TypeError(f"Path conflict at '{k}'")
                d = nxt

            leaf = keys[-1]
            old = d.get(leaf)
            new = fn(old)
            d[leaf] = new
            return new
