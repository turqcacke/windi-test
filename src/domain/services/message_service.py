from domain.chat import Chat, ChatMember, ChatType
from domain.message import Message
from domain.shared import Event, EventPullable, MessageSeenEvent


class MessageManagerService(EventPullable[Event]):
    def __init__(self):
        self._events = list()

    def is_seen_by_all(self, chat: Chat, message: Message):
        seen = False
        if chat.type == ChatType.GROUP or chat.type == ChatType.PERSONAL:
            seen = len(message.seen_by) == len(chat.participants)
            if seen and not message.is_seen():
                self._events.append(MessageSeenEvent(chat.id, message.id))
        return seen

    def can_add_message(self, chat: Chat, message: Message) -> bool:
        return ChatMember(message.sender_id) in chat.participants
