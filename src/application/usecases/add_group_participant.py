import datetime
from dataclasses import dataclass
from typing import Any

from application.exceptions import (
    ChatDoesNoeExists,
    GroupDoesNotExists,
    UserDoesNotExists,
)
from application.ports.live_chat_service import LiveChatMessageDTO, LiveChatService
from application.uow import UnitOfWork
from domain.chat import ChatType


@dataclass
class AddGroupParticipantDTO:
    group_id: int
    user_id: int
    initiator_id: int


class AddGroupParticipantUseCase:
    def __init__(self, uow: UnitOfWork[Any]):
        self._uow = uow

    async def execute(self, add_participant_data: AddGroupParticipantDTO):
        async with self._uow as uow:
            group = await uow.container.group_repository.get_group(
                add_participant_data.group_id
            )

            if not group:
                raise GroupDoesNotExists(
                    f"Unable to find group id={add_participant_data.group_id}."
                )

            chat = await uow.container.chat_repository.get_chat_by_entity_type(
                group.id, ChatType.GROUP
            )
            if not chat:
                raise ChatDoesNoeExists(
                    f"Unable to find chat with id={group.id},type={ChatType.GROUP}."
                )
            if not await uow.container.user_repository.get_user(
                user_id=add_participant_data.user_id
            ):
                raise UserDoesNotExists(
                    f"Unable to find user with id={add_participant_data.user_id}"
                )

            chat.add_participant(
                add_participant_data.initiator_id, add_participant_data.user_id
            )
            group.add_participant(
                add_participant_data.initiator_id, add_participant_data.user_id
            )

            uow.seen.append(chat)

            await uow.container.chat_repository.save(chat)
            await uow.container.group_repository.save(group)

            await uow.commit()
