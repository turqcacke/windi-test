import datetime
from dataclasses import dataclass, field
from enum import IntEnum, auto
from typing import Any

from domain.shared import Event, EventPullable

from .events import UserJoindedChatEvent
from .exceptions import AlreadyChatMember, InvalidInitiator


class ChatType(IntEnum):
    PERSONAL = auto()
    GROUP = auto()


@dataclass
class ChatMember:
    user_id: int
    id: int | None = field(default=None)

    def __eq__(self, value: Any):
        if isinstance(value, self.__class__):
            return self.user_id == value.user_id
        return False


@dataclass
class Chat(EventPullable[Event]):
    id: int
    type: ChatType
    entity_id: int
    participants: list[ChatMember]
    _events: list[Event] = field(default_factory=lambda: list())

    def add_participant(self, initiator_id: int, user_id: int):
        if not self.is_participant(initiator_id):
            raise InvalidInitiator()
        member = ChatMember(user_id)
        if member not in self.participants:
            self.participants.append(member)
            self._events.append(
                UserJoindedChatEvent(
                    chat_id=self.id,
                    user_id=user_id,
                    timestamp=datetime.datetime.now(datetime.UTC),
                )
            )
            return
        raise AlreadyChatMember()

    def is_participant(self, user_id: int) -> bool:
        return ChatMember(user_id) in self.participants
