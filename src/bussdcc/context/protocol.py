from typing import Protocol, Callable, Any, TYPE_CHECKING

from bussdcc.clock import Clock
from bussdcc.event.engine import Subscription
from bussdcc.event.protocol import EventEngineProtocol
from bussdcc.state.protocol import StateEngineProtocol

if TYPE_CHECKING:
    from bussdcc.runtime.protocol import RuntimeProtocol

EventHandler = Callable[..., None]


class ContextProtocol(Protocol):
    clock: Clock
    runtime: "RuntimeProtocol"
    events: EventEngineProtocol
    state: StateEngineProtocol
