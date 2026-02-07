from typing import Protocol

from bussdcc.device import DeviceProtocol
from bussdcc.context import ContextProtocol


class RuntimeProtocol(Protocol):
    ctx: ContextProtocol

    def get_device(self, name: str) -> DeviceProtocol | None: ...
    def list_devices(self) -> list[str]: ...
