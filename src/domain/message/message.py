import datetime
from dataclasses import dataclass


@dataclass
class SeenBy:
    message_id: str
    user_id: str
    at: datetime.datetime


@dataclass
class Message:
    id: int
    chat_id: int
    sender_id: int
    text: str
    timestamp: datetime.datetime
    seen_by: list[SeenBy]
    _seen: bool = False

    def add_to_seen_by(self, user_id: int):
        if user_id not in self.seen_by:
            self.seen_by.append(user_id)

    def mark_as_seen(self):
        self._seen = True

    def is_seen(self) -> bool:
        return self._seen
