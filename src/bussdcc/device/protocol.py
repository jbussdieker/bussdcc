from typing import Protocol

from bussdcc.context import ContextProtocol


class DeviceProtocol(Protocol):
    """
    Protocol for a device.
    Devices can attach to a context, manage their lifecycle, and report status.
    """

    name: str
    ctx: "ContextProtocol | None"
    online: bool

    def attach(self, ctx: "ContextProtocol") -> None: ...
    def detach(self) -> None: ...
    def connect(self) -> None: ...
    def disconnect(self) -> None: ...
