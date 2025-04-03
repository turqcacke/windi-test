from sqlalchemy.ext.asyncio import AsyncSession

from application.exceptions import InvalidChatInterraction, MessageDoesNotExists
from application.uow import UnitOfWork
from domain.services.message_service import MessageManagerService


class MarkMessageAsSeenUseCase:
    def __init__(
        self,
        uow: UnitOfWork[AsyncSession],
        message_manage_service: MessageManagerService,
    ):
        self._uow = uow
        self._message_manage_service = message_manage_service

    async def execute(self, user_id: int, message_id: int):
        async with self._uow as uow:
            message = await uow.container.message_repository.get_message(
                message_id=message_id
            )
            if not message:
                raise MessageDoesNotExists(f"Message {message_id} does not exists.")

            chat = await uow.container.chat_repository.get_chat(message.chat_id)

            if not chat.is_participant(user_id):
                raise InvalidChatInterraction(f"User {user_id} is not chat member.")

            message.add_to_seen_by(user_id)

            if self._message_manage_service.is_seen_by_all(chat, message):
                message.mark_as_seen()

            await uow.container.message_repository.save(message)
