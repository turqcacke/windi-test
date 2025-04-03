import pytest
from faker import Faker

from application.exceptions import ChatDoesNoeExists, UnableToAddMessage
from application.usecases.add_message_to_chat import (
    AddMessageToChatDTO,
    AddMessageToChatUseCase,
)
from domain.chat import Chat, ChatMember, ChatType
from domain.message import Message
from domain.services import MessageManagerService
from domain.user import User
from tests.utils.fakes import FakeUowFactory
from tests.utils.fakes.ports import FakeLiveChatService


@pytest.mark.asyncio
class TestAddMessageToChat:
    async def test_should_add_message_successfully(self, faker: Faker):
        user = User(
            id=1, name=faker.name(), email=faker.email(), password_hash=faker.uuid4()
        )
        chat = Chat(
            id=10,
            type=ChatType.GROUP,
            participants=[ChatMember(user_id=user.id)],
            entity_id=100,
        )
        dto = AddMessageToChatDTO(
            chat_id=chat.id,
            sender_id=user.id,
            text="Hello!",
        )

        messages: list[Message] = []

        uow = FakeUowFactory(chats=[chat], users=[user], messages=messages, groups=[])
        livechat_service = FakeLiveChatService(joined=True)
        usecase = AddMessageToChatUseCase(
            uow, MessageManagerService(), livechat_service
        )

        await usecase.execute(dto)

        assert uow.committed
        assert any(dto.text == msg.text for msg in messages)
        assert any(msg.data == dto.text for msg in livechat_service.messages)
        assert len(uow.seen) > 1

    async def test_should_raise_when_chat_not_found(self, faker: Faker):
        user = User(
            id=1, name=faker.name(), email=faker.email(), password_hash=faker.uuid4()
        )
        dto = AddMessageToChatDTO(
            chat_id=999,
            sender_id=user.id,
            text=faker.words(nb=10),
        )

        uow = FakeUowFactory(chats=[], users=[user], messages=[], groups=[])
        livechat_service = FakeLiveChatService(joined=True)
        usecase = AddMessageToChatUseCase(
            uow, MessageManagerService(), livechat_service
        )

        with pytest.raises(ChatDoesNoeExists):
            await usecase.execute(dto)

    async def test_should_raise_when_user_not_in_chat(self, faker: Faker):
        user = User(
            id=1, name=faker.name(), email=faker.email(), password_hash=faker.uuid4()
        )
        chat = Chat(
            id=10,
            type=ChatType.GROUP,
            participants=[],
            entity_id=100,
        )
        dto = AddMessageToChatDTO(
            chat_id=chat.id,
            sender_id=user.id,
            text=faker.words(nb=10),
        )

        uow = FakeUowFactory(chats=[chat], users=[user], messages=[], groups=[])
        livechat_service = FakeLiveChatService(joined=True)
        usecase = AddMessageToChatUseCase(
            uow, MessageManagerService(), livechat_service
        )
        with pytest.raises(UnableToAddMessage):
            await usecase.execute(dto)
