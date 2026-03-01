import traceback

from bussdcc.event import Event
from bussdcc.context import ContextProtocol
from bussdcc.message import Message, EventLevel
from bussdcc import message

from .protocol import ProcessProtocol


class Process(ProcessProtocol):
    name = "unnamed"

    ctx: ContextProtocol | None

    def _handle_event(self, evt: Event[Message]) -> None:
        if self.ctx is None:
            return
        try:
            self.handle_event(self.ctx, evt)
        except Exception as e:
            # Never recurse on error-level events
            if evt.payload.level >= EventLevel.ERROR:
                return

            self.ctx.emit(
                message.ProcessError(
                    process=self.name,
                    error=repr(e),
                    evt=evt,
                    traceback=traceback.format_exc(),
                )
            )

    def attach(self, ctx: ContextProtocol) -> None:
        self.ctx = ctx
        self._sub = ctx.events.subscribe(Message, self._handle_event)

    def detach(self) -> None:
        self.ctx = None
        self._sub.cancel()

    def start(self, ctx: ContextProtocol) -> None:
        pass

    def stop(self, ctx: ContextProtocol) -> None:
        pass

    def handle_event(self, ctx: ContextProtocol, evt: Event[Message]) -> None:
        pass
