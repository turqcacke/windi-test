import pytest

from domain.shared.event import EventPullable


class FakeEvent:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, FakeEvent) and self.name == other.name


class DummyEventSource(EventPullable[FakeEvent]):
    def __init__(self, initial_events: list[FakeEvent]):
        self._events = initial_events


class TestEventPullable:
    @pytest.mark.parametrize(
        "initial_events, expected_first_pull, expected_second_pull",
        [
            ([], [], []),  # No events
            ([FakeEvent("a")], [FakeEvent("a")], []),  # One event
            (
                [FakeEvent("a"), FakeEvent("b")],
                [FakeEvent("a"), FakeEvent("b")],
                [],
            ),  # Two events
        ],
    )
    def test_pull_events(
        self,
        initial_events: list[FakeEvent],
        expected_first_pull: list[FakeEvent],
        expected_second_pull: list[FakeEvent],
    ):
        source = DummyEventSource(initial_events.copy())

        first_pull = source.pull_events()
        second_pull = source.pull_events()

        assert first_pull == expected_first_pull
        assert second_pull == expected_second_pull
