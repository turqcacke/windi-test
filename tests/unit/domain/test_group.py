from typing import Callable

import pytest
from faker import Faker

from domain.group import Group


class TestGroup:
    @pytest.mark.parametrize(
        "new_participant_getter,iter_times",
        [
            [lambda p: p[0], 1],  # Existing
            [lambda p: max(p) + 1, 1],  # New
            [lambda p: p[0], 10],  # Existing 10 time
            [lambda p: max(p) + 1, 10],  # New 10 times
        ],
    )
    def test_group_add_participant(
        self,
        faker: Faker,
        new_participant_getter: Callable[[list[int]], int],
        iter_times: int,
    ):
        group = Group(
            id=faker.random_int(),
            title=faker.color_name(),
            owner_id=faker.random_int(),
            participants=[i for i in range(100)],
        )
        for _ in range(iter_times):
            new_group_participant = new_participant_getter(group.participants)
            group.add_participant(new_group_participant)
            assert new_group_participant in group.participants
