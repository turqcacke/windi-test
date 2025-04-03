from typing import Callable

import pytest
from faker import Faker

from domain.group import Group, GroupMember
from domain.group.exceptions import AlreadyGroupMember, InvalidInitiator
from tests.utils.helpers import dummy_contextmanager


class TestGroup:
    @pytest.mark.parametrize(
        "new_member_getter, initiator_getter, iter_times, exc",
        [
            # Existing participant, valid initiator
            (
                lambda p: p[0].user_id,
                lambda p: p[1].user_id,
                1,
                AlreadyGroupMember,
            ),
            # New participant, valid initiator
            (
                lambda p: max(p, key=lambda v: v.user_id).user_id + 1,
                lambda p: p[0].user_id,
                1,
                None,
            ),
            # New participant, invalid initiator
            (
                lambda p: max(p, key=lambda v: v.user_id).user_id + 1,
                lambda p: max(p, key=lambda v: v.user_id).user_id + 10,
                1,
                InvalidInitiator,
            ),
            # Existing participant, 10 times
            (
                lambda p: p[0].user_id,
                lambda p: p[1].user_id,
                10,
                AlreadyGroupMember,
            ),
            # New participant, 10 times
            (
                lambda p: max(p, key=lambda v: v.user_id).user_id + 1,
                lambda p: p[0].user_id,
                10,
                None,
            ),
        ],
    )
    def test_group_add_participant(
        self,
        faker: Faker,
        new_member_getter: Callable[[list[GroupMember]], int],
        initiator_getter: Callable[[list[GroupMember]], int],
        iter_times: int,
        exc: type[Exception] | None,
    ):
        group = Group(
            id=faker.random_int(),
            title=faker.color_name(),
            owner_id=faker.random_int(),
            participants=[GroupMember(i) for i in range(100)],
        )

        ctx = pytest.raises if exc else dummy_contextmanager

        for _ in range(iter_times):
            user_id = new_member_getter(group.participants)
            initiator_id = initiator_getter(group.participants)

            with ctx(exc):
                group.add_participant(initiator_id=initiator_id, user_id=user_id)
                assert GroupMember(user_id) in group.participants

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
        group = Group(
            id=faker.random_int(),
            title=faker.color_name(),
            owner_id=faker.random_int(),
            participants=[GroupMember(i) for i in participants],
        )
        assert group.is_participant(check_user_id) == expected
