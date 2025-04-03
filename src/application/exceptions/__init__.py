from .base import UseCaseException
from .exceptions import (
    ChatDoesNoeExists,
    GroupDoesNotExists,
    InvalidChatInterraction,
    MessageDoesNotExists,
    UnableToAddMessage,
    UseCaseExceptionCoverter,
    UserDoesNotExists,
)


def as_usecase_exc():
    return UseCaseExceptionCoverter()
