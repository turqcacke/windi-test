from typing import Any

from application.uow import UnitOfWork
from domain.chat import ChatType


class AddGroupParticipantUseCase:
    def __init__(self, uow: UnitOfWork[Any]):
        self._uow = uow

    async def execute(self, group_id: int, user_id: int):
        async with self._uow as uow:
            group = await uow.container.group_repository.get_group(group_id)

            if not group:
                raise  # TODO Group does not exists

            chat = await uow.container.chat_repository.get_chat_by_entity_type(
                group.id, ChatType.GROUP
            )
            if not chat:
                raise  # TODO Chat deos not exists
            if not await uow.container.user_repository.get_user(user_id=user_id):
                raise  # TODO User does not exists

            chat.add_particiapnt(user_id)
            group.add_participant(user_id)

            await uow.container.chat_repository.save(chat)
            await uow.container.group_repository.save(group)

            await uow.commit()
