from dataclasses import dataclass
from typing import Type, TypeVar, Generic

ConfigT = TypeVar("ConfigT")
DriverT = TypeVar("DriverT")


@dataclass(slots=True, frozen=True)
class DeviceDefinition(Generic[ConfigT, DriverT]):
    config_class: Type[ConfigT]
    driver_class: Type[DriverT]
