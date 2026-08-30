from typing import Optional

from .client import BaleClient
from .types import Message


class Bot:
    def __init__(self, token: str):
        self.client = BaleClient(token)

    async def start(self):
        await self.client.connect()
        return self

    async def stop(self):
        await self.client.close()

    async def send_message(
        self,
        chat_id: str,
        text: str,
    ):
        return await self.client.call(
            "Messaging",
            "SendMessage",
            chat_id=chat_id,
            text=text,
        )

    async def get_user(self, user_id: str):
        return await self.client.call(
            "Users",
            "GetUser",
            user_id=user_id,
        )

    async def get_chat(self, chat_id: str):
        return await self.client.call(
            "Groups",
            "GetChat",
            chat_id=chat_id,
        )