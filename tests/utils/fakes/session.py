class DummySession:
    async def close(self):
        return

    async def commit(self):
        return

    async def rollback(self):
        return
