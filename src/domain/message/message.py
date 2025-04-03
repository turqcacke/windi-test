import datetime
from dataclasses import dataclass, field
from typing import Self


@dataclass
class SeenBy:
    user_id: str
    at: datetime.datetime
    id: int | None = None

    def __eq__(self, value: int | Self):
        if isinstance(value, SeenBy):
            return self.user_id == value.user_id
        if isinstance(value, int):
            return self.user_id == value
        return super().__eq__(value)


@dataclass
class Message:
    chat_id: int
    sender_id: int
    text: str
    seen_by: list[SeenBy]
    _seen: bool = False
    id: int | None = field(default=None)
    timestamp: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )

    def add_to_seen_by(self, user_id: int):
        seen_by = SeenBy(user_id, datetime.datetime.now(datetime.UTC))
        if user_id not in self.seen_by:
            self.seen_by.append(seen_by)

    def mark_as_seen(self):
        self._seen = True

    def is_seen(self) -> bool:
        return self._seen
