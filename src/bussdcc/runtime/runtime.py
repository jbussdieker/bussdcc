from typing import Optional, Dict

from bussdcc.context import Context, ContextProtocol
from bussdcc.clock import Clock, SystemClock
from bussdcc.device import DeviceProtocol
from bussdcc.event import EventEngine
from bussdcc.version import get_version

from .protocol import RuntimeProtocol


class Runtime(RuntimeProtocol):
    def __init__(self, *, clock: Optional[Clock] = None):
        self.clock: Clock = clock or SystemClock()
        self.events = EventEngine(clock=self.clock)
        self._devices: Dict[str, DeviceProtocol] = {}
        # type-safe context using RuntimeProtocol
        self.ctx: ContextProtocol = Context(
            clock=self.clock, runtime=self, events=self.events
        )
        self._booted: bool = False
        self.version: str = get_version()

    def register_device(self, device: DeviceProtocol) -> None:
        if self._booted:
            raise RuntimeError("Cannot register devices after boot")
        self._devices[device.name] = device

    def get_device(self, name: str) -> DeviceProtocol | None:
        """Retrieve a registered device by name."""
        return self._devices.get(name)

    def list_devices(self) -> list[str]:
        """Return a list of registered device names."""
        return list(self._devices.keys())

    def boot(self) -> None:
        if self._booted:
            return

        self.ctx.emit("system.booting", version=self.version)

        # Boot all registered devices
        for device in self._devices.values():
            device.attach(self.ctx)

        self._booted = True
        self.ctx.emit("system.booted", version=self.version)

    def shutdown(self, reason: Optional[str] = None) -> None:
        self.ctx.emit("system.shutting_down")

        # Detach devices in reverse order
        for device in reversed(list(self._devices.values())):
            device.detach()

        self.ctx.emit("system.shutdown")
