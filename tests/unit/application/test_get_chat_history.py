import pytest
from faker import Faker

from application.exceptions import InvalidChatInterraction
from application.usecases.get_chat_history import GetChatHistoryUseCase
from domain.chat import Chat, ChatMember, ChatType
from domain.message import Message
from domain.services.message_service import MessageManagerService
from tests.utils.fakes import FakeUowFactory
from tests.utils.helpers import dummy_contextmanager


@pytest.mark.asyncio
class TestGetChatHistory:
    @pytest.mark.parametrize(
        "paticipants,initiator,exc",
        [
            ([1, 2], 1, None),  # User is member
            ([1, 2], 3, InvalidChatInterraction),  # User is not a member
        ],
    )
    async def test_execute(
        self, faker: Faker, paticipants: list[int], initiator: int, exc: type[Exception]
    ):
        context_manager = dummy_contextmanager if not exc else pytest.raises
        chat = Chat(
            id=faker.random_int(),
            type=ChatType.GROUP,
            entity_id=faker.random_int(),
            participants=[ChatMember(i) for i in paticipants],
        )
        messages = [
            Message(
                id=i,
                chat_id=chat.id,
                sender_id=faker.random_int(),
                text=faker.words(2),
                seen_by=[],
            )
            for i in range(100)
        ]
        uow = FakeUowFactory(chats=[chat], messages=messages)
        usecase = GetChatHistoryUseCase(uow, MessageManagerService())
        with context_manager(exc):
            result = await usecase.execute(
                initiator_id=initiator, chat_id=chat.id, limit=10, last_seen_id=5
            )
            assert result[0].id == 5
            assert len(result) == 10
