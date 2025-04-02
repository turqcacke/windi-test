import datetime
from dataclasses import dataclass, field
from enum import IntEnum, auto

from domain.shared import Event, EventPullable

from .events import UserJoindedChatEvent


class ChatType(IntEnum):
    PERSONAL = auto()
    GROUP = auto()


@dataclass
class Chat(EventPullable[Event]):
    id: int
    type: ChatType
    participants: list[int]
    _events: list[Event] = field(default_factory=lambda: list())

    def add_particiapnt(self, user_id: int):
        if user_id not in self.participants:
            self.participants.append(user_id)
            self._events.append(
                UserJoindedChatEvent(
                    chat_id=self.id,
                    user_id=user_id,
                    timestamp=datetime.datetime.now(datetime.UTC),
                )
            )
