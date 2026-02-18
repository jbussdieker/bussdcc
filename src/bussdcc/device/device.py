from bussdcc.device import DeviceProtocol
from bussdcc.context import ContextProtocol


class Device(DeviceProtocol):
    kind: str = "device"
    id: str
    ctx: ContextProtocol | None
    online: bool

    def __init__(self, *, id: str) -> None:
        self.id = id
        self.ctx = None
        self.online = False

    def attach(self, ctx: ContextProtocol) -> None:
        self.ctx = ctx
        try:
            self.connect()
        except Exception as e:
            if self.ctx:
                self.ctx.events.emit(
                    "device.failed", device=self.id, kind=self.kind, error=repr(e)
                )
            raise
        self.online = True
        if self.ctx:
            self.ctx.events.emit("device.attached", device=self.id, kind=self.kind)

    def detach(self) -> None:
        try:
            self.disconnect()
        except Exception as e:
            if self.ctx:
                self.ctx.events.emit(
                    "device.failed", device=self.id, kind=self.kind, error=repr(e)
                )
        finally:
            self.online = False
            if self.ctx:
                self.ctx.events.emit("device.detached", device=self.id, kind=self.kind)
            self.ctx = None

    def connect(self) -> None:
        """Open hardware / resources"""
        pass

    def disconnect(self) -> None:
        """Close hardware / resources"""
        pass
