from typing import Dict

from bussdcc.context import ContextProtocol
from bussdcc.process import ProcessProtocol
from bussdcc import message


class InterfaceManager:
    def __init__(self, ctx: ContextProtocol):
        self._ctx = ctx
        self._interfaces: Dict[str, ProcessProtocol] = {}

    def register(self, interface: ProcessProtocol) -> None:
        if interface.name in self._interfaces:
            raise ValueError(f"Interface `{interface.name}` already registered")

        self._interfaces[interface.name] = interface

    def list(self) -> list[ProcessProtocol]:
        return list(self._interfaces.values())

    def boot(self) -> None:
        for interface in self._interfaces.values():
            interface.attach(self._ctx)
            interface.start(self._ctx)
            self._ctx.emit(message.InterfaceStarted(interface=interface.name))

    def shutdown(self) -> None:
        for interface in reversed(list(self._interfaces.values())):
            try:
                interface.stop(self._ctx)
            finally:
                interface.detach()
                self._ctx.emit(message.InterfaceStopped(interface=interface.name))
