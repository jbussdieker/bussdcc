from typing import Dict

from bussdcc.device import DeviceProtocol
from bussdcc.context import ContextProtocol


class DeviceManager:
    def __init__(self, ctx: ContextProtocol):
        self._ctx = ctx
        self._devices: Dict[str, DeviceProtocol] = {}

    def attach(self, device: DeviceProtocol, *, booted: bool) -> None:
        if device.id in self._devices:
            raise ValueError(f"Device {device.id} already attached")

        self._devices[device.id] = device

        if booted:
            device.attach(self._ctx)

    def detach(self, id: str) -> None:
        device = self._devices.pop(id, None)
        if device:
            device.detach()

    def get(self, id: str) -> DeviceProtocol | None:
        return self._devices.get(id)

    def list(self, *, kind: str | None = None) -> list[DeviceProtocol]:
        if kind is None:
            return list(self._devices.values())

        return [d for d in self._devices.values() if d.kind == kind]

    def boot(self) -> None:
        for device in self._devices.values():
            device.attach(self._ctx)

    def shutdown(self) -> None:
        for device in reversed(list(self._devices.values())):
            device.detach()
