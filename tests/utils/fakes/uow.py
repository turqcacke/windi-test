from application.uow import UnitOfWork

from .container import DummySession, FakeContainer


class FakeUoW(UnitOfWork[DummySession]):
    def __init__(self, session, container, message_bus):
        super().__init__(session, container, message_bus)
        self.committed = False

    async def commit(self):
        self.committed = True
        await self._session.rollback()

    async def close(self):
        await self._session.rollback()

    async def rollback(self):
        await self._session.rollback()
