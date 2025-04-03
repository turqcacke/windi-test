import abc
from typing import Any, Protocol, Type

from domain.shared import Event


class EventHandler[T: Event](Protocol):
    @abc.abstractmethod
    async def handle(self, event: T) -> None | Any: ...


class MessageBus(EventHandler):
    def __init__(self, default_handler: EventHandler[Event]):
        self._handlers: dict[Type, EventHandler[Event]] = {}
        self._default_handler = default_handler

    def register(self, event_class: Type[Event], event_handler: EventHandler[Event]):
        self._handlers.update({event_class: event_handler})

    async def handle(self, event: Any) -> Any:
        handler = self._handlers.get(type(event), self._default_handler)
        return await handler.handle(event)
