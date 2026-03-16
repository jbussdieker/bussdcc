from typing import Protocol, Optional

from bussdcc.device import DeviceProtocol, DeviceManagerProtocol
from bussdcc.context import ContextProtocol
from bussdcc.interface import InterfaceManager, InterfaceManagerProtocol
from bussdcc.process import ProcessManager, ProcessManagerProtocol
from bussdcc.service import ServiceSupervisor, ServiceSupervisorProtocol


class RuntimeProtocol(Protocol):
    ctx: ContextProtocol
    interfaces: InterfaceManagerProtocol
    processes: ProcessManagerProtocol
    devices: DeviceManagerProtocol
    services: ServiceSupervisorProtocol

    @property
    def booted(self) -> bool: ...

    def boot(self) -> None: ...
    def run(self) -> None: ...
    def shutdown(self, reason: Optional[str] = None) -> None: ...
