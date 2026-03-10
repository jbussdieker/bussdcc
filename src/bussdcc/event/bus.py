from typing import List, TypeVar, cast
from collections import deque
import traceback
import threading

from .event import Event
from .handler import TypedHandler
from .protocol import EventHandler, SubscriptionProtocol, EventBusProtocol

from ..message import Message, Severity
from .. import message

T = TypeVar("T")


class _Subscription:
    def __init__(self, engine: "EventBus", handler: TypedHandler[T]):
        self._engine = engine
        self._handler = handler
        self._cancelled = False

    def cancel(self) -> None:
        if not self._cancelled:
            self._engine._unsubscribe(self)
            self._cancelled = True


class EventBus(EventBusProtocol):
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._subscriptions: List[_Subscription] = []

    def subscribe(
        self, event_type: type[T], handler: EventHandler[T]
    ) -> SubscriptionProtocol:
        wrapped = TypedHandler(event_type, handler)
        sub = _Subscription(self, wrapped)
        with self._lock:
            self._subscriptions.append(sub)
        return sub

    def _unsubscribe(self, subscription: _Subscription) -> None:
        with self._lock:
            try:
                self._subscriptions.remove(subscription)
            except ValueError:
                pass

    def unsubscribe(self, subscription: SubscriptionProtocol) -> None:
        subscription.cancel()

    def emit(self, evt: Event[Message]) -> None:
        queue = deque([evt])

        with self._lock:
            subs = list(self._subscriptions)

        while queue:
            current = queue.popleft()

            for sub in subs:
                try:
                    sub._handler.handle(current)
                except Exception as e:
                    # Never recurse on error-level events
                    if current.payload.severity >= Severity.ERROR:
                        continue

                    try:
                        error_evt = Event(
                            time=current.time,
                            payload=cast(
                                Message,
                                message.EventSubscriberError(
                                    event=current.payload._key(),
                                    handler=repr(sub._handler),
                                    error=repr(e),
                                    traceback=traceback.format_exc(),
                                ),
                            ),
                        )

                        queue.append(error_evt)

                    except Exception:
                        # Absolute last-resort safety
                        pass
