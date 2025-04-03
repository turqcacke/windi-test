from typing import Callable

import pytest
from faker import Faker

from domain.chat import Chat, ChatMember, ChatType
from domain.chat.exceptions import AlreadyChatMember, InvalidInitiator
from tests.utils.helpers import dummy_contextmanager


class TestChat:
    @pytest.mark.parametrize(
        "new_member_getter,initator_getter,iter_times,exc",
        [
            [
                lambda p: max(p, key=lambda v: v.user_id).user_id + 1,
                lambda p: p[0].user_id,
                1,
                None,
            ],  # New participant
            [
                lambda p: p[0].user_id,
                lambda p: p[1].user_id,
                1,
                AlreadyChatMember,
            ],  # Existing participant
            [
                lambda p: max(p, key=lambda v: v.user_id).user_id + 1,
                lambda p: max(p, key=lambda v: v.user_id).user_id + 2,
                1,
                InvalidInitiator,
            ],  # Non existing initator new participant
            [
                lambda p: max(p, key=lambda v: v.user_id).user_id + 1,
                lambda p: p[0].user_id,
                10,
                None,
            ],  # New participant 10 times
        ],
    )
    def test_add_participatns(
        self,
        faker: Faker,
        new_member_getter: Callable[[list[int]], int],
        initator_getter: Callable[[list[int]], int],
        iter_times: int,
        exc: type[Exception],
    ):
        chat = Chat(
            id=faker.random_int(),
            type=faker.random_element([ChatType.GROUP, ChatType.PERSONAL]),
            participants=[ChatMember(i) for i in range(1, 100)],
            entity_id=faker.random_int(),
        )
        exception_context_manager = dummy_contextmanager if not exc else pytest.raises
        for _ in range(iter_times):
            new_participant = new_member_getter(chat.participants)
            initiator = initator_getter(chat.participants)
            with exception_context_manager(exc):
                chat.add_participant(initiator_id=initiator, user_id=new_participant)
                assert ChatMember(new_participant) in chat.participants

    @pytest.mark.parametrize(
        "participants,check_user_id,expected",
        [
            [[i for i in range(10)], 10, False],  # Negative case
            [[i for i in range(10)], 0, True],  # Positive case
        ],
    )
    def test_is_participant(
        self, faker: Faker, participants: list[int], check_user_id: int, expected: bool
    ):
        chat = Chat(
            id=faker.random_int(),
            type=faker.random_element([ChatType.GROUP, ChatType.PERSONAL]),
            participants=[ChatMember(i) for i in participants],
            entity_id=faker.random_int(),
        )
        assert chat.is_participant(check_user_id) == expected
