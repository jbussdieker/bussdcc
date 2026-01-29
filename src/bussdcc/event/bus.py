from typing import DefaultDict, List, Any
from collections import defaultdict

from .protocol import EventBusProtocol, EventHandler


class EventBus(EventBusProtocol):
    def __init__(self) -> None:
        self._listeners: DefaultDict[str, List[EventHandler]] = defaultdict(list)

    def on(self, event: str, handler: EventHandler) -> None:
        self._listeners[event].append(handler)

    def emit(self, event: str, **kwargs: Any) -> None:
        for handler in self._listeners[event]:
            handler(**kwargs)
