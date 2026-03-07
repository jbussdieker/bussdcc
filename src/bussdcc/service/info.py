from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ServiceInfo:
    name: str
    running: bool
    enabled: bool
    attached: bool
    interval: float
    restart: bool
    critical: bool
