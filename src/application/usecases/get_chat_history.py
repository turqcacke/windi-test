from sqlalchemy.ext.asyncio import AsyncSession

from application.exceptions import InvalidChatInterraction
from application.ports import LiveChatService
from application.uow import UnitOfWork
from domain.chat import Chat
from domain.message import Message
from domain.services import MessageManagerService
from tests.utils.fakes import uow


class GetChatHistoryUseCase:
    def __init__(
        self,
        uow: UnitOfWork[AsyncSession],
        message_manage_service: MessageManagerService,
    ):
        self._uow = uow
        self._message_manage_service = message_manage_service

    async def execute(
        self,
        initiator_id: int,
        chat_id: int,
        limit: int,
        last_seen_id: int | None = None,
    ) -> list[Message]:
        async with self._uow as uow:
            chat = await uow.container.chat_repository.get_chat(chat_id)
            if not chat.is_participant(initiator_id):
                raise InvalidChatInterraction(
                    f"User {initiator_id} is not part of chat"
                )
            return await uow.container.message_repository.chat_history(
                chat_id=chat_id, limit=limit, last_seen_id=last_seen_id
            )
