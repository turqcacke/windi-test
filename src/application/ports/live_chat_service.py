import abc
import datetime
from typing import Literal, Protocol

from pydantic import BaseModel

from domain.chat.chat import Chat


class EventDataDTO(BaseModel):
    event: str
    user_id: int | None = None
    message_id: int | None = None


class LiveChatMessageDTO(BaseModel):
    chat_id: int
    sender_id: int
    data: str | EventDataDTO
    timestamp: datetime.datetime
    type: Literal["message", "notification"]


class LiveChatService(Protocol):

    @abc.abstractmethod
    async def join(self, chat_id: int, user_id: int) -> None: ...
    @abc.abstractmethod
    async def leave(self, chat_id: int, user_id: int) -> None: ...
    @abc.abstractmethod
    async def send_message(self, message: LiveChatMessageDTO) -> None: ...
