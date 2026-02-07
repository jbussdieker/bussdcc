from typing import Dict, Any
from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    time: str
    name: str
    data: Dict[str, Any]
