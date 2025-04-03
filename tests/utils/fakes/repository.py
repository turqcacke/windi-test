from application.repository import (
    ChatRepository,
    GroupRepository,
    MessageRepository,
    UserRepository,
)
from domain.chat import Chat, ChatType
from domain.group import Group, GroupMember
from domain.message import Message
from domain.user import User


class FakeChatRepository(ChatRepository):

    def __init__(self, initial_chats: list[Chat]):
        self.chat_list = initial_chats

    async def get_chat(self, chat_id: int) -> Chat | None:
        chat = filter(lambda e: e.id == chat_id, self.chat_list)
        return next(chat, None)

    async def get_chat_by_entity_type(self, entity_id: int, type: ChatType):
        chat = filter(
            lambda e: e.entity_id == entity_id and e.type == type, self.chat_list
        )
        return next(chat, None)

    async def save(self, chat: Chat):
        entity = next(filter(lambda e: e.id == chat.id, self.chat_list), None)
        if not entity:
            self.chat_list.remove(self.chat_list.index(entity))
        self.chat_list.append(chat)
        return True


class FakeGroupRepository(GroupRepository):

    def __init__(self, initial_groups: list[Group]):
        self.group_list = initial_groups

    async def get_group(self, group_id: int) -> Group | None:
        group = filter(lambda g: g.id == group_id, self.group_list)
        return next(group, None)

    async def save(self, group: Group):
        entity = next(filter(lambda e: e.id == group.id, self.group_list), None)
        if not entity:
            self.group_list.remove(self.group_list.index(entity))
        self.group_list.append(group)
        return True


class FakeMessageRepository(MessageRepository):

    def __init__(self, initial: list[Message]):
        self.message_list: list[Message] = initial

    async def get_message(self, message_id) -> Message | None:
        return next(filter(lambda m: m.id == message_id, self.message_list), None)

    async def add_message(self, message: Message):
        self.message_list.append(message)
        return message

    async def chat_history(self, chat_id, limit, last_seen_id) -> list[Message]:
        element = next(filter(lambda m: m.id == last_seen_id, self.message_list), None)
        index = (
            self.message_list.index(element)
            if element in self.message_list
            else len(self.message_list)
        )
        return [
            msg
            for msg in self.message_list[index : index + limit]
            if msg.chat_id == chat_id
        ]

    async def save(self, message: Message):
        entity = next(filter(lambda m: m.id == message.id, self.message_list), None)
        if not entity:
            self.message_list.remove(self.message_list.index(entity))
        self.message_list.append(message)


class FakeUserRepository(UserRepository):

    def __init__(self, initial_users: list[User]):
        self.user_list = initial_users

    async def get_user(self, user_id: int) -> User | None:
        user = filter(lambda u: u.id == user_id, self.user_list)
        return next(user, None)
