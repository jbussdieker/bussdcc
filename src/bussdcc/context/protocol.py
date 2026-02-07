from typing import Protocol, TYPE_CHECKING

from bussdcc.clock import Clock
from bussdcc.event.protocol import EventEngineProtocol
from bussdcc.state.protocol import StateEngineProtocol

if TYPE_CHECKING:
    from bussdcc.runtime.protocol import RuntimeProtocol


class ContextProtocol(Protocol):
    clock: Clock
    runtime: "RuntimeProtocol"
    events: EventEngineProtocol
    state: StateEngineProtocol
