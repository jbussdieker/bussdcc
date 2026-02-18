from abc import abstractmethod

from bussdcc.event.event import Event
from bussdcc.context import ContextProtocol

from .protocol import ProcessProtocol


class Process(ProcessProtocol):
    name = "unnamed"
    ctx: ContextProtocol | None

    def _handle_event(self, evt: Event) -> None:
        if self.ctx is None:
            return
        try:
            self.handle_event(self.ctx, evt)
        except Exception as e:
            self.ctx.events.emit(
                "process.error",
                process=self.name,
                error=repr(e),
                evt=evt.name,
            )

    def attach(self, ctx: ContextProtocol) -> None:
        self.ctx = ctx
        self._sub = ctx.events.subscribe(self._handle_event)

    def detach(self) -> None:
        self.ctx = None
        self._sub.cancel()

    def start(self, ctx: ContextProtocol) -> None:
        pass

    def stop(self, ctx: ContextProtocol) -> None:
        pass

    @abstractmethod
    def handle_event(self, ctx: ContextProtocol, evt: Event) -> None:
        pass
