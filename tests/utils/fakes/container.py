from faker import Faker

from application.repository.container import Conatiner
from domain.chat.chat import Chat
from domain.group import Group
from domain.message import Message
from domain.user import User

from .repository import (
    FakeChatRepository,
    FakeGroupRepository,
    FakeMessageRepository,
    FakeUserRepository,
)
from .session import DummySession


class FakeContainer(Conatiner[DummySession]):
    def __init__(
        self,
        chats: list[Chat] | None = None,
        users: list[User] | None = None,
        groups: list[Group] | None = None,
        messages: list[Message] | None = None,
    ):
        super().__init__()
        self.chats = [] if chats is None else chats
        self.users = [] if users is None else users
        self.groups = [] if groups is None else groups
        self.messages = [] if messages is None else messages

    def initialize(self, session):
        self.chat_repository = FakeChatRepository(self.chats)
        self.group_repository = FakeGroupRepository(self.groups)
        self.message_repository = FakeMessageRepository(self.messages)
        self.user_repository = FakeUserRepository(self.users)
        self._initalized = True
        return self
