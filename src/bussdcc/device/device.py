from bussdcc.device import DeviceProtocol
from bussdcc.context import ContextProtocol


class Device(DeviceProtocol):
    name: str = "unnamed"
    ctx: ContextProtocol | None
    online: bool

    def __init__(self) -> None:
        self.ctx = None
        self.online = False

    def attach(self, ctx: ContextProtocol) -> None:
        self.ctx = ctx
        try:
            self.connect()
        except Exception as e:
            if self.ctx:
                self.ctx.emit("device.failed", device=self.name, error=repr(e))
            raise
        self.online = True
        if self.ctx:
            self.ctx.emit("device.attached", device=self.name)

    def detach(self) -> None:
        try:
            self.disconnect()
        finally:
            self.online = False
            if self.ctx:
                self.ctx.emit("device.detached", device=self.name)

    def connect(self) -> None:
        """Open hardware / resources"""
        pass

    def disconnect(self) -> None:
        """Close hardware / resources"""
        pass
