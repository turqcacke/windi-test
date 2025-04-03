from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from application.exceptions import ChatDoesNoeExists, UnableToAddMessage
from application.ports import LiveChatMessageDTO, LiveChatService
from application.uow import UnitOfWork
from domain.message import Message
from domain.services import MessageManagerService
from domain.shared import NewMessageEvent


@dataclass
class AddMessageToChatDTO:
    chat_id: int
    sender_id: str
    text: str

    def to_domain(self) -> Message:
        return Message(
            chat_id=self.chat_id, sender_id=self.sender_id, text=self.text, seen_by=[]
        )


class AddMessageToChatUseCase:
    def __init__(
        self,
        uow: UnitOfWork[AsyncSession],
        message_manage_service: MessageManagerService,
        livechat_service: LiveChatService,
    ):
        self._uow = uow
        self._message_manage_service = message_manage_service
        self._chat_service = livechat_service

    async def execute(self, message_data: AddMessageToChatDTO):
        message = message_data.to_domain()
        async with self._uow as uow:
            chat = await uow.container.chat_repository.get_chat(message.chat_id)
            if not chat:
                raise ChatDoesNoeExists(
                    f"Unable to find chat with id={message.chat_id}."
                )
            if not self._message_manage_service.can_add_message(chat, message):
                raise UnableToAddMessage(
                    f"Initiator {message_data.sender_id} is not member of chat."
                )

            message = await uow.container.message_repository.add_message(message)
            await self._chat_service.send_message(
                LiveChatMessageDTO(
                    chat_id=chat.id,
                    sender_id=message.sender_id,
                    data=message.text,
                    timestamp=message.timestamp,
                    type="message",
                )
            )
            uow.push_event(
                NewMessageEvent(message.chat_id, chat.participants, message.timestamp)
            )
            uow.seen.append(self._message_manage_service)
            await uow.commit()
