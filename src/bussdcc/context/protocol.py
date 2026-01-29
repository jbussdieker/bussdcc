from typing import Protocol, Callable, Any, TYPE_CHECKING

from bussdcc.clock import Clock
from bussdcc.event.engine import Subscription

if TYPE_CHECKING:
    from bussdcc.runtime.protocol import RuntimeProtocol

EventHandler = Callable[..., None]


class ContextProtocol(Protocol):
    clock: Clock
    runtime: "RuntimeProtocol"

    def sleep(self, seconds: float) -> None: ...
    def emit(self, event: str, **kwargs: Any) -> None: ...
    def on(self, handler: Callable[..., None]) -> Subscription: ...
