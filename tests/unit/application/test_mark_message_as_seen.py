import datetime

import pytest
from faker import Faker

from application.exceptions.exceptions import (
    InvalidChatInterraction,
    MessageDoesNotExists,
)
from application.usecases.mark_message_as_seen import MarkMessageAsSeenUseCase
from domain.chat.chat import Chat, ChatMember, ChatType
from domain.message import Message, SeenBy
from domain.services.message_service import MessageManagerService
from tests.conftest import faker
from tests.utils.fakes import FakeUowFactory
from tests.utils.helpers import dummy_contextmanager


@pytest.mark.asyncio()
class TestMarkMessagesSeen:
    @pytest.mark.parametrize(
        "participants,seen_by,user_id,message_id,exc",
        [
            # User not seen
            ([1, 2, 3], [1, 2], 3, 1, None),
            # User not in chat
            ([1, 2], [1], 99, 1, InvalidChatInterraction),
            # Message not seen
            ([1, 2], [1], 2, 999, MessageDoesNotExists),
            # User seen
            ([1, 2, 3], [1, 2, 3], 3, 1, None),
            # All seen
            ([1, 2], [1], 2, 1, None),
        ],
    )
    async def test_execute(
        self,
        faker: Faker,
        participants: list[int],
        seen_by: list[int],
        user_id: int,
        message_id: int,
        exc: type[Exception],
    ):
        context_manager = dummy_contextmanager if not exc else pytest.raises
        chat = Chat(
            id=faker.random_int(),
            type=ChatType.GROUP,
            entity_id=faker.random_int(),
            participants=[ChatMember(i) for i in participants],
        )
        message = Message(
            id=1,
            chat_id=chat.id,
            sender_id=faker.random_int(),
            text=faker.words(2),
            seen_by=[
                SeenBy(
                    user_id=i, at=faker.date_time(datetime.UTC), id=faker.random_int()
                )
                for i in seen_by
            ],
        )
        uow = FakeUowFactory(chats=[chat], messages=[message])
        usecase = MarkMessageAsSeenUseCase(uow, MessageManagerService())

        with context_manager(exc):
            await usecase.execute(user_id=user_id, message_id=message_id)
