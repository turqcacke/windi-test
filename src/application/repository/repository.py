import abc
from typing import Protocol

from domain.chat import Chat, ChatType
from domain.group import Group
from domain.message import Message
from domain.user import User


class GroupRepository(Protocol):
    @abc.abstractmethod
    async def get_group(self, group_id: int) -> Group | None: ...

    @abc.abstractmethod
    async def save(save, group: Group) -> bool: ...


class MessageRepository(Protocol):
    @abc.abstractmethod
    async def get_message(self, message_id) -> Message: ...
    @abc.abstractmethod
    async def add_message(self, message: Message) -> Message: ...
    @abc.abstractmethod
    async def chat_history(
        self, chat_id: int, limit: int, last_seen_id: int
    ) -> list[Message]: ...
    @abc.abstractmethod
    async def save(self, message: Message) -> None: ...


class ChatRepository(Protocol):
    @abc.abstractmethod
    async def get_chat(self, chat_id: int) -> Chat | None: ...

    @abc.abstractmethod
    async def get_chat_by_entity_type(
        self, entity_id: int, type: ChatType
    ) -> Chat | None: ...

    @abc.abstractmethod
    async def save(self, chat: Chat) -> bool: ...


class UserRepository(Protocol):
    @abc.abstractmethod
    async def get_user(self, user_id: int) -> User: ...
