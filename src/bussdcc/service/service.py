from bussdcc.event.event import Event
from bussdcc.context.protocol import ContextProtocol

from .protocol import ServiceProtocol


class Service(ServiceProtocol):
    name = "unnamed"

    # execution model
    interval = 1.0  # seconds between ticks
    enabled = True  # start at boot
    restart = True  # restart if it crashes
    critical = False  # if True, system may halt on failure

    ctx: ContextProtocol | None

    def _handle_event(self, evt: Event) -> None:
        if self.ctx is None:
            return
        try:
            self.handle_event(self.ctx, evt)
        except Exception as e:
            self.ctx.events.emit(
                "service.error",
                service=self.name,
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
        """Called once when the service starts"""
        pass

    def tick(self, ctx: ContextProtocol) -> None:
        """Called repeatedly while the service is running"""
        pass

    def stop(self, ctx: ContextProtocol) -> None:
        """Called once when the service is stopping"""
        pass

    def handle_event(self, ctx: ContextProtocol, evt: Event) -> None:
        pass
