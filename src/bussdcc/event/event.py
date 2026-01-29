from collections import deque
from dataclasses import dataclass
from typing import Callable, Deque, Dict, Any


@dataclass(frozen=True)
class Event:
    time: str
    name: str
    data: Dict[str, Any]
