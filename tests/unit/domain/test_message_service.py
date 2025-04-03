import pytest
from faker import Faker

from domain.chat.chat import Chat, ChatMember, ChatType
from domain.message import Message
from domain.services.message_service import MessageManagerService


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
        service = MessageManagerService()
        chat = Chat(
            id=faker.random_int(),
            type=chat_type,
            participants=[ChatMember(i, i) for i in range(participant_count)],
            entity_id=faker.random_int(),
        )

        message = Message(
            id=faker.random_int(),
            chat_id=chat.id,
            sender_id=faker.random_int(),
            text=faker.text(),
            timestamp=faker.date_time(),
            seen_by=[i for i in range(seen_by_count)],
        )

        result = service.is_seen_by_all(chat, message)
        events_fit = result == bool(len(service._events))

        assert result is expected and events_fit

    @pytest.mark.parametrize(
        "chat_memebers, sender, expected",
        [
            [[i for i in range(10)], 3, True],  # Group chat member exists
            [[i for i in range(10)], 11, False],  # Group chat member not exists
            [[31, 44], 31, True],  # Personal chat
        ],
    )
    def test_can_add_message(
        self, faker: Faker, chat_memebers: list[int], sender: int, expected: bool
    ):
        chat = Chat(
            id=faker.random_int(),
            type=ChatType,
            participants=[ChatMember(i, i) for i in chat_memebers],
            entity_id=faker.random_int(),
        )
        message = Message(
            chat_id=faker.random_int(),
            sender_id=sender,
            text=faker.text(max_nb_chars=128),
            seen_by=[],
        )
        service = MessageManagerService()
        assert service.can_add_message(chat, message) is expected
