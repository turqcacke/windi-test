import abc

from domain.group import Group


class GroupRepository:
    @abc.abstractmethod
    async def get_group(self, group_id: int) -> Group | None: ...

    @abc.abstractmethod
    async def save(save, group: Group) -> bool: ...
