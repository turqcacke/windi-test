from typing import Protocol


class Event(Protocol): ...


class EventPullable[T: Event](Protocol):
    _events: list[T]

    def pull_events(self) -> list[T]:
        events = self._events.copy()
        self._events.clear()
        return events
