import pytest
from faker import Faker

from domain.chat.chat import Chat, ChatType
from domain.message import Message
from domain.services.read_service import MessageReadService


class TestMessageReadService:

    @pytest.mark.parametrize(
        "chat_type, seen_by_count, participant_count, expected",
        [
            (ChatType.GROUP, 3, 3, True),  # All read
            (ChatType.GROUP, 2, 3, False),  # Not all read
            (ChatType.PERSONAL, 2, 2, True),  # All read (personal)
            (ChatType.PERSONAL, 1, 2, False),  # Not all read(pearsonal)
            (-1, 10, 10, False),  # Unsupported Type
        ],
    )
    def test_is_seen_by_all(
        self,
        faker: Faker,
        chat_type: ChatType,
        seen_by_count: int,
        participant_count: int,
        expected: bool,
    ):
        chat = Chat(
            id=faker.random_int(),
            type=chat_type,
            participants=[i for i in range(participant_count)],
        )

        message = Message(
            id=faker.random_int(),
            chat_id=chat.id,
            sender_id=faker.random_int(),
            text=faker.text(),
            timestamp=faker.date_time(),
            seen_by=[i for i in range(seen_by_count)],
        )

        result = MessageReadService.is_seen_by_all(chat, message)

        assert result is expected
