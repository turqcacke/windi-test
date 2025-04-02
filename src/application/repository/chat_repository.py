import abc
from typing import Optional, Protocol

from domain.chat import Chat, ChatType


class ChatRepository:
    @abc.abstractmethod
    async def get_chat(self, chat_id: int) -> Chat | None: ...

    @abc.abstractmethod
    async def get_chat_by_entity_type(
        self, entity_id: int, type: ChatType
    ) -> Chat | None: ...

    @abc.abstractmethod
    async def save(self, chat: Chat) -> bool: ...
