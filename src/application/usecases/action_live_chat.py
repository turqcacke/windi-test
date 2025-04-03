from dataclasses import dataclass
from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession

from application.exceptions import (
    ChatDoesNoeExists,
    InvalidChatInterraction,
    UserDoesNotExists,
)
from application.ports import LiveChatService
from application.uow import UnitOfWork


class JoinLiveChatUseCase:
    def __init__(
        self, uow: UnitOfWork[AsyncSession], livechat_service: LiveChatService
    ):
        self._uow = uow
        self._livechat_service = livechat_service

    async def execute(
        self, chat_id: int, user_id: int, action: Literal["join", "leave"]
    ):
        async with self._uow as uow:
            chat = await uow.container.chat_repository.get_chat(chat_id)
            user = await uow.container.user_repository.get_user(user_id)
            if not user:
                raise UserDoesNotExists(f"User {user_id} does not exists.")
            if not chat:
                raise ChatDoesNoeExists(f"Chat {chat_id} does not exists.")
            if not chat.is_participant(user_id):
                raise InvalidChatInterraction(
                    f"User({user_id}) is not part of Chat({chat_id})."
                )
            match action:
                case "join":
                    await self._livechat_service.join(chat_id, user_id)
                case "leave":
                    await self._livechat_service.leave(chat_id, user_id)
