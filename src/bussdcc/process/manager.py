from typing import Dict

from bussdcc.context import ContextProtocol
from bussdcc.process import ProcessProtocol
from bussdcc import message


class ProcessManager:
    def __init__(self, ctx: ContextProtocol):
        self._ctx = ctx
        self._processes: Dict[str, ProcessProtocol] = {}

    def register(self, process: ProcessProtocol) -> None:
        if process.name in self._processes:
            raise ValueError(f"Process `{process.name}` already registered")

        self._processes[process.name] = process

    def list(self) -> list[ProcessProtocol]:
        return list(self._processes.values())

    def boot(self) -> None:
        for process in self._processes.values():
            process.attach(self._ctx)
            process.start(self._ctx)
            self._ctx.emit(message.ProcessStarted(process=process.name))

    def shutdown(self) -> None:
        for process in self._processes.values():
            try:
                process.stop(self._ctx)
            finally:
                process.detach()
                self._ctx.emit(message.ProcessStopped(process=process.name))
