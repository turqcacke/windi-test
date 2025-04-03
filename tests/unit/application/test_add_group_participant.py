import pytest
from faker import Faker

from application.exceptions import ChatDoesNoeExists, GroupDoesNotExists
from application.exceptions.exceptions import UserDoesNotExists
from application.usecases.add_group_participant import (
    AddGroupParticipantDTO,
    AddGroupParticipantUseCase,
)
from domain.chat import Chat, ChatMember, ChatType
from domain.group import Group, GroupMember
from domain.user import User
from tests.utils.fakes import FakeUowFactory


@pytest.mark.asyncio
class TestAddGroupParticipantUseCase:

    async def test_execute_success(self, faker: Faker):
        user_list = [
            User(
                id=uid,
                name=faker.name(),
                email=faker.email(),
                password_hash=faker.uuid4(),
            )
            for uid in range(3)
        ]

        owner = user_list[0]
        participants = user_list[:-1]
        user_add = user_list[-1]

        group = Group(
            id=faker.random_int(),
            title=faker.color_name(),
            owner_id=owner.id,
            participants=[GroupMember(user_id=user.id) for user in participants],
        )

        chat = Chat(
            id=faker.random_int(),
            type=ChatType.GROUP,
            participants=[ChatMember(user_id=user.id) for user in participants],
            entity_id=group.id,
        )

        uow = FakeUowFactory(chats=[chat], groups=[group], users=user_list, messages=[])
        usecase = AddGroupParticipantUseCase(uow)

        await usecase.execute(
            AddGroupParticipantDTO(
                group_id=group.id, user_id=user_add.id, initiator_id=owner.id
            )
        )

        assert any(p.user_id == user_add.id for p in chat.participants)
        assert any(p.user_id == user_add.id for p in group.participants)

    async def test_should_raise_when_group_not_found(self, faker: Faker):
        user = User(
            id=1,
            name=faker.name(),
            email=faker.email(),
            password_hash=faker.uuid4(),
        )

        uow = FakeUowFactory(chats=[], groups=[], users=[user], messages=[])
        usecase = AddGroupParticipantUseCase(uow)

        with pytest.raises(GroupDoesNotExists):
            await usecase.execute(
                AddGroupParticipantDTO(
                    group_id=999, user_id=user.id, initiator_id=user.id
                )
            )

    async def test_should_raise_when_chat_not_found(self, faker: Faker):
        user = User(
            id=1, name=faker.name(), email=faker.email(), password_hash=faker.uuid4()
        )

        group = Group(
            id=1,
            title="Test Group",
            owner_id=user.id,
            participants=[GroupMember(user_id=user.id)],
        )

        uow = FakeUowFactory(chats=[], groups=[group], users=[user], messages=[])
        usecase = AddGroupParticipantUseCase(uow)

        with pytest.raises(ChatDoesNoeExists):
            await usecase.execute(
                AddGroupParticipantDTO(
                    group_id=group.id, user_id=user.id, initiator_id=user.id
                )
            )

    async def test_should_raise_when_user_not_found(self, faker: Faker):
        owner = User(
            id=1, name=faker.name(), email=faker.email(), password_hash=faker.uuid4()
        )

        group = Group(
            id=1,
            title="Test Group",
            owner_id=owner.id,
            participants=[GroupMember(user_id=owner.id)],
        )

        chat = Chat(
            id=10,
            type=ChatType.GROUP,
            entity_id=group.id,
            participants=[ChatMember(user_id=owner.id)],
        )

        uow = FakeUowFactory(chats=[chat], groups=[group], users=[owner], messages=[])
        usecase = AddGroupParticipantUseCase(uow)

        with pytest.raises(UserDoesNotExists):
            await usecase.execute(
                AddGroupParticipantDTO(
                    group_id=group.id, user_id=42, initiator_id=owner.id
                )
            )
