from typing import Protocol

from bussdcc.device import DeviceProtocol
from bussdcc.context import ContextProtocol


class RuntimeProtocol(Protocol):
    ctx: ContextProtocol

    @property
    def booted(self) -> bool: ...
