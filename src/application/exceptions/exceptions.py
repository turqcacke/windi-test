from typing import Any, Awaitable, Callable

from application.exceptions.base import UseCaseException
from domain.shared.exceptions import DomainExecption

_AsyncFunction = Callable[[int], Awaitable[Any]]


class UserDoesNotExists(UseCaseException): ...


class ChatDoesNoeExists(UseCaseException): ...


class InvalidChatInterraction(UseCaseException): ...


class GroupDoesNotExists(UseCaseException): ...


class UserDoesNotExists(UseCaseException): ...


class MessageDoesNotExists(UseCaseException): ...


class UnableToAddMessage(UseCaseException): ...


class UseCaseExceptionCoverter:
    def __call__(self, func: _AsyncFunction, *args, **kwds) -> _AsyncFunction:
        async def wraps(*args, **kwargs) -> Any:
            try:
                return await func(*args, **kwargs)
            except DomainExecption as e:
                raise UseCaseException(e.message)

        return wraps
