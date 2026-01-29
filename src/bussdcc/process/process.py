from abc import abstractmethod

from bussdcc.event.event import Event
from bussdcc.context import Context, ContextProtocol

from .protocol import ProcessProtocol


class Process(ProcessProtocol):
    name = "unnamed"

    def _on_event(self, evt: Event) -> None:
        try:
            self.on_event(self.ctx, evt)
        except Exception as e:
            self.ctx.emit(
                "process.error",
                process=self.name,
                error=repr(e),
                evt=evt.name,
            )

    def attach(self, ctx: ContextProtocol) -> None:
        self.ctx = ctx
        self._sub = ctx.events.subscribe(self._on_event)
        self.on_start(ctx)
        self.ctx.emit("process.started", process=self.name)

    def detach(self) -> None:
        try:
            self._sub.cancel()
            self.on_stop(self.ctx)
        finally:
            self.ctx.emit("process.stopped", process=self.name)

    def on_start(self, ctx: ContextProtocol) -> None:
        pass

    def on_stop(self, ctx: ContextProtocol) -> None:
        pass

    @abstractmethod
    def on_event(self, ctx: ContextProtocol, event: Event) -> None:
        pass
