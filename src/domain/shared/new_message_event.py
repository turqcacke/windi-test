import datetime
from dataclasses import dataclass

from .event import Event


@dataclass
class NewMessageEvent(Event):
    chat_id: int
    notify: list[int]
    timestamp: datetime.datetime
