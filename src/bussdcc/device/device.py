import traceback
from typing import Optional, TypeVar, Generic

from bussdcc.device import DeviceProtocol
from bussdcc.context import ContextProtocol
from bussdcc import message

ConfigT = TypeVar("ConfigT")


class Device(Generic[ConfigT], DeviceProtocol[ConfigT]):
    kind: str = "device"
    id: str
    ctx: Optional[ContextProtocol]

    def __init__(self, *, id: str, config: Optional[ConfigT] = None):
        self.id = id
        self.ctx = None
        self._config = config
        self._online = False

    @property
    def online(self) -> bool:
        return self._online

    @property
    def config(self) -> ConfigT:
        if self._config is None:
            raise RuntimeError("Device not configured")
        return self._config

    def set_online(self) -> None:
        if not self._online:
            self._online = True
            if self.ctx:
                self.ctx.emit(message.DeviceOnline(device=self.id, kind=self.kind))

    def set_offline(self, error: Optional[Exception] = None) -> None:
        if self._online:
            self._online = False
            if self.ctx:
                self.ctx.emit(
                    message.DeviceOffline(
                        device=self.id,
                        kind=self.kind,
                        error=repr(error) if error else None,
                    )
                )

    def attach(self, ctx: ContextProtocol) -> None:
        self.ctx = ctx
        try:
            self.connect()
        except Exception as e:
            if self.ctx:
                self.ctx.emit(
                    message.DeviceFailed(
                        device=self.id,
                        kind=self.kind,
                        error=repr(e),
                        traceback=traceback.format_exc(),
                    )
                )
            raise

        if self.ctx:
            self.ctx.emit(message.DeviceAttached(device=self.id, kind=self.kind))

        self.set_online()

    def detach(self) -> None:
        try:
            self.disconnect()
        except Exception as e:
            if self.ctx:
                self.ctx.emit(
                    message.DeviceFailed(
                        device=self.id,
                        kind=self.kind,
                        error=repr(e),
                        traceback=traceback.format_exc(),
                    )
                )
        finally:
            self.set_offline()
            if self.ctx:
                self.ctx.emit(message.DeviceDetached(device=self.id, kind=self.kind))
            self.ctx = None

    def connect(self) -> None:
        """Open hardware / resources"""
        pass

    def disconnect(self) -> None:
        """Close hardware / resources"""
        pass
