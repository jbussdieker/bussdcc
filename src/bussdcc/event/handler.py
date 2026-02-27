from typing import Callable, Generic, TypeVar, cast

from .event import Event

T = TypeVar("T")


class TypedHandler(Generic[T]):
    def __init__(
        self,
        event_type: type[T],
        handler: Callable[[Event[T]], None],
    ):
        self._event_type = event_type
        self._handler = handler

    def handle(self, event: Event[object]) -> None:
        if isinstance(event.payload, self._event_type):
            self._handler(cast(Event[T], event))
