import abc

from domain.user import User


class UserRepository:
    @abc.abstractmethod
    async def get_user(self, user_id: int) -> User: ...
