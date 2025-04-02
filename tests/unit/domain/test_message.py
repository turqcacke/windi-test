import datetime

import pytest
from faker import Faker

from domain.message import Message


class TestMessage:
    @pytest.mark.parametrize(
        "initial_seen_by,user_to_mark,expected_count",
        [
            ([], 42, 1),
            ([1, 2, 3], 2, 3),
            ([1, 2, 3], 4, 4),
        ],
    )
    def test_add_to_seen_by(
        self,
        faker: Faker,
        initial_seen_by: list[int],
        user_to_mark: int,
        expected_count: int,
    ):
        message = Message(
            id=faker.random_int(),
            chat_id=faker.random_int(),
            sender_id=faker.random_int(),
            text="Hello!",
            timestamp=faker.date_time(),
            seen_by=initial_seen_by.copy(),
        )

        message.add_to_seen_by(user_to_mark)

        assert user_to_mark in message.seen_by
        assert len(message.seen_by) == expected_count

    def test_mark_as_seen_sets_flag_true(self, faker: Faker):
        msg = Message(
            id=faker.random_int(),
            chat_id=faker.random_int(),
            sender_id=faker.date_time(),
            text="Hi",
            timestamp=datetime.datetime.now(datetime.UTC),
            seen_by=[],
        )

        assert not msg.is_seen()

        msg.mark_as_seen()

        assert msg.is_seen()
