from typing import Protocol, TYPE_CHECKING

from bussdcc.clock import ClockProtocol
from bussdcc.message import Message
from bussdcc.event.protocol import EventBusProtocol
from bussdcc.state.protocol import StateStoreProtocol

if TYPE_CHECKING:
    from bussdcc.runtime.protocol import RuntimeProtocol


class ContextProtocol(Protocol):
    clock: ClockProtocol
    runtime: "RuntimeProtocol"
    events: EventBusProtocol
    state: StateStoreProtocol

    def emit(self, message: Message) -> None: ...
