from dataclasses import dataclass

from .event import Event


@dataclass
class MessageSeenEvent:
    chat_id: int
    message_id: int
