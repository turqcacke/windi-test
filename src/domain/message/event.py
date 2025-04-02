from dataclasses import dataclass


@dataclass
class MassageSeenEvent:
    chat_id: int
    message_id: int
