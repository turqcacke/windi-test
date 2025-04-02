from abc import abstractmethod
from typing import Callable, Protocol, Self

from sqlalchemy.ext.asyncio import AsyncSession

from application.repository.container import Conatiner


class UnitOfWork[T](Protocol):
    def __init__(self, session: Callable[..., T], container: Conatiner[AsyncSession]):
        self._container = container
        self._session = session

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

    async def __aexit__(self, *args):
        self._session = None
        await self.close()
        return

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def close(self): ...

    @abstractmethod
    async def rollback(self): ...
