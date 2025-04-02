from dataclasses import dataclass

from domain.shared import Event


@dataclass
class UserJoindedChatEvent(Event):
    chat_id: int
    user_id: int
    timestamp: int
