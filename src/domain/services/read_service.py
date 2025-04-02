from domain.chat import Chat, ChatType
from domain.message import Message, SeenBy


class MessageReadService:
    @staticmethod
    def is_seen_by_all(chat: Chat, message: Message) -> bool:
        if chat.type == ChatType.GROUP or chat.type == ChatType.PERSONAL:
            return len(message.seen_by) == len(chat.participants)
        return False
