from abc import abstractmethod

from bussdcc.context.protocol import ContextProtocol

from .protocol import InterfaceProtocol


class Interface(InterfaceProtocol):
    name = "unnamed"

    def attach(self, ctx: ContextProtocol) -> None:
        self.ctx = ctx
        self.on_start(ctx)
        self.ctx.emit("interface.started", interface=self.name)

    def detach(self) -> None:
        try:
            self.on_stop(self.ctx)
        finally:
            self.ctx.emit("interface.stopped", interface=self.name)

    @abstractmethod
    def on_start(self, ctx: ContextProtocol) -> None:
        """Called when interface is attached."""
        pass

    @abstractmethod
    def on_stop(self, ctx: ContextProtocol) -> None:
        """Called when interface is detached."""
        pass
