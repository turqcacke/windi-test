from dataclasses import dataclass
from typing import Any

import pytest

from application.message_bus import EventHandler, MessageBus
from domain.shared.event import Event


@dataclass
class DummyEvent(Event):
    data: Any


@dataclass
class IntDummyEvent(Event):
    data: int


@dataclass
class StrDummyEvent(Event):
    data: str


class DummyEventHandler(EventHandler[DummyEvent]):
    async def handle(self, event: DummyEvent):
        return self.__class__.__name__


class IntDummyEventHandler(EventHandler[IntDummyEvent]):
    async def handle(self, event: IntDummyEvent):
        return self.__class__.__name__


class StrDummyEventHandler(EventHandler[StrDummyEvent]):
    async def handle(self, event: StrDummyEvent):
        return self.__class__.__name__


@pytest.mark.asyncio(loop_scope="class")
class TestMessageBus:

    @pytest.mark.parametrize(
        "class_to_handler,event,result",
        [
            [
                [(IntDummyEvent, IntDummyEventHandler())],
                IntDummyEvent(data=1),
                IntDummyEventHandler.__name__,
            ],  # One event handler
            [
                [
                    (StrDummyEvent, StrDummyEventHandler()),
                    (IntDummyEvent, IntDummyEventHandler()),
                ],
                StrDummyEvent(data="Event"),
                StrDummyEventHandler.__name__,
            ],  # Two event handlers
            [
                [],
                StrDummyEvent(data="Event"),
                DummyEventHandler.__name__,
            ],  # No event hadnlers
        ],
    )
    async def test_register(
        self,
        class_to_handler: list[tuple[type[Event], EventHandler]],
        event: Event,
        result: str,
    ):
        message_bus = MessageBus(DummyEventHandler())

        for clazz, handler in class_to_handler:
            message_bus.register(clazz, handler)

        handle_result = await message_bus.handle(event)
        assert handle_result == result
