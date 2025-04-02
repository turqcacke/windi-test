from typing import Callable

import pytest
from faker import Faker

from domain.chat import Chat, ChatType


class TestChat:
    @pytest.mark.parametrize(
        "new_participant_getter,iter_times",
        [
            [lambda p: max(p) + 1, 1],  # New participant
            [lambda p: p[0], 1],  # Existing participant
            [lambda p: max(p) + 1, 10],  # New participant
            [lambda p: p[0], 10],  # Existing participant
        ],
    )
    def test_add_participatns(
        self,
        faker: Faker,
        new_participant_getter: Callable[[list[int]], int],
        iter_times: int,
    ):
        chat = Chat(
            id=faker.random_int(),
            type=faker.random_element([ChatType.GROUP, ChatType.PERSONAL]),
            participants=[i for i in range(1, 100)],
        )
        for _ in range(iter_times):
            new_participant = new_participant_getter(chat.participants)
            new_participant_getter(chat.participants)
            chat.add_particiapnt(user_id=new_participant)

            assert new_participant in chat.participants
