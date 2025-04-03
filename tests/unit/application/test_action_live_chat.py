import pytest
from faker import Faker

from application.exceptions.exceptions import (
    ChatDoesNoeExists,
    InvalidChatInterraction,
    UserDoesNotExists,
)
from application.usecases.action_live_chat import JoinLiveChatUseCase
from domain.chat import Chat
from domain.chat.chat import ChatMember, ChatType
from domain.user import User
from tests.utils.fakes import FakeLiveChatService, FakeUowFactory
from tests.utils.helpers import dummy_contextmanager


class TestActionLiveChat:
    @pytest.mark.parametrize(
        "action,chats,users,exc,joined_result",
        [
            ("join", [1], [1, 1], None, True),  # Member
            ("join", [1], [], UserDoesNotExists, True),  # Unexistent user
            ("join", [], [1], ChatDoesNoeExists, True),  # Unexistent chat
            ("join", [1], [1, 2], InvalidChatInterraction, True),  # Not a chat member
            ("leave", [1], [1, 1], None, False),  # Member
            ("leave", [1], [], UserDoesNotExists, False),  # Unexistent user
            ("leave", [], [1], ChatDoesNoeExists, False),  # Unexistent chat
            ("leave", [1], [2], InvalidChatInterraction, False),  # Not a chat member
        ],
    )
    @pytest.mark.asyncio
    async def test_action_livechat_usecase(
        self,
        faker: Faker,
        action: str,
        chats: list[int],
        users: list[int],
        exc: type[Exception],
        joined_result: bool,
    ):
        user_objs = [
            User(
                id=uid,
                name=faker.name(),
                email=faker.email(),
                password_hash=faker.uuid4(),
            )
            for uid in set(users)
        ]

        chat_objs = [
            Chat(
                id=cid,
                type=ChatType.GROUP,
                entity_id=faker.random_int(),
                participants=[ChatMember(u) for u in users[:-1]],
            )
            for cid in chats
        ]

        uow = FakeUowFactory(chat_objs, user_objs, [], [])
        service = FakeLiveChatService(joined=not joined_result)
        usecase = JoinLiveChatUseCase(uow, service)

        context_manager = dummy_contextmanager if not exc else pytest.raises

        target_chat_id = chat_objs[0].id if chat_objs else faker.random_int()
        target_user_id = users[-1] if users else faker.random_int()

        with context_manager(exc):
            await usecase.execute(
                chat_id=target_chat_id,
                user_id=target_user_id,
                action=action,
            )
            assert service.joined == joined_result
