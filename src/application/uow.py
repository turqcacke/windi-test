from abc import abstractmethod
from typing import Callable, Protocol, Self

from sqlalchemy.ext.asyncio import AsyncSession

from application.message_bus import MessageBus
from application.repository.container import Conatiner
from domain.shared import Event, EventPullable


class UnitOfWorkEventStore(EventPullable[Event]):
    def __init__(self):
        self._events = []

    def add_event(self, event: Event):
        self._events.append(event)


class UnitOfWork[T](Protocol):
    def __init__(
        self,
        session: T,
        container: Conatiner[AsyncSession],
        message_bus: MessageBus,
    ):
        self._container = container
        self._session = session
        self._message_bus = message_bus
        self._event_store = UnitOfWorkEventStore()
        self.seen: list[EventPullable] = [self._event_store]

    @property
    def container(self):
        if not self._container.is_initialized():
            raise ValueError("Container should be initialized before usage.")
        return self._container

    def _get_session(self) -> T:
        return self._session

    async def __aenter__(self) -> Self:
        session = self._get_session()
        self._container.initialize(session)
        return self

    async def __aexit__(self, exc_type, *args):
        if exc_type:
            await self.rollback()
        else:
            await self.close()
            await self._publish_events()
        self.container.reset()
        self._session = None

    async def _publish_events(self):
        for entity in self.seen:
            for event in entity.pull_events():
                await self._message_bus.handle(event)

    def push_event(self, event: Event):
        self._event_store.add_event(event)

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def close(self): ...

    @abstractmethod
    async def rollback(self): ...
