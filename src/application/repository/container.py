import abc
from typing import Protocol, Self

from application.repository import ChatRepository, GroupRepository, UserRepository


class Conatiner[T](Protocol):
    chat_repository: ChatRepository
    group_repository: GroupRepository
    user_repository: UserRepository

    def __init__(self):
        self._initalized = False

    @abc.abstractmethod
    def initialize(self, session: T) -> Self: ...

    def is_initialized(self):
        return self._initalized
