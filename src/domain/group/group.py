from dataclasses import dataclass, field
from typing import Any

from .exceptions import AlreadyGroupMember, InvalidInitiator


@dataclass
class GroupMember:
    user_id: int
    id: int | None = field(default=None)

    def __eq__(self, value: Any):
        if isinstance(value, self.__class__):
            return self.user_id == value.user_id
        return False


@dataclass
class Group:
    id: int
    title: str
    owner_id: int
    participants: list[GroupMember]

    def add_participant(self, initiator_id: int, user_id: int):
        if not self.is_participant(initiator_id):
            raise InvalidInitiator()
        member = GroupMember(user_id)
        if member not in self.participants:
            self.participants.append(member)
            return
        raise AlreadyGroupMember()

    def is_participant(self, user_id: int) -> bool:
        return GroupMember(user_id) in self.participants
