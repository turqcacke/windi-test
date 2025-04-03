from application.ports import LiveChatMessageDTO, LiveChatService


class FakeLiveChatService(LiveChatService):
    def __init__(self, joined: bool = False):
        self.messages: list[LiveChatMessageDTO] = []
        self.joined = joined

    async def send_message(self, message):
        self.messages.append(message)

    async def join(self, chat_id, user_id):
        self.joined = True

    async def leave(self, chat_id, user_id):
        self.joined = False
