from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Event:
    time: datetime
    name: str
    data: Dict[str, Any]
