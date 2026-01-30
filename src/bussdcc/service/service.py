from bussdcc.context.protocol import ContextProtocol

from .protocol import ServiceProtocol


class Service(ServiceProtocol):
    name = "unnamed"

    # execution model
    interval = 1.0  # seconds between ticks
    enabled = True  # start at boot
    restart = True  # restart if it crashes
    critical = False  # if True, system may halt on failure

    def start(self, ctx: ContextProtocol) -> None:
        """Called once when the service starts"""
        pass

    def tick(self, ctx: ContextProtocol) -> None:
        """Called repeatedly while the service is running"""
        pass

    def stop(self, ctx: ContextProtocol) -> None:
        """Called once when the service is stopping"""
        pass
