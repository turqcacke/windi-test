from email.headerregistry import Group
from mailbox import Message

from application.message_bus import MessageBus
from domain.chat.chat import Chat
from domain.user.user import User

from .container import FakeContainer
from .ports import FakeLiveChatService
from .session import DummySession
from .uow import FakeUoW


def FakeUowFactory(
    chats: list[Chat] | None = None,
    users: list[User] | None = None,
    messages: list[Message] | None = None,
    groups: list[Group] | None = None,
):
    container = FakeContainer(chats, users, groups, messages)

    async def dummy_handle(*args, **kargs):
        return

    dummy_handler = type("DummyHandler", (), {})()
    dummy_handler.handle = dummy_handle

    return FakeUoW(
        session=DummySession(),
        container=container,
        message_bus=MessageBus(dummy_handler),
    )
