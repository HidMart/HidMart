import asyncio

from .events import NewMessage
from .handlers import HandlerManager
from .models import (
    Message,
    User,
    Chat
)
from .transport import WebTransport


class SelfBot:

    def __init__(
        self,
        session,
        poll_interval=1.0,
        timeout=30,
        endpoint=None
    ):
        self.session = session

        self.poll_interval = poll_interval

        self.transport = WebTransport(
            session,
            endpoint=endpoint,
            timeout=timeout
        )

        self.handlers = HandlerManager()

        self._running = False

    def on_message(self, pattern=None):

        event = NewMessage(pattern)

        def decorator(callback):

            async def wrapper(message):

                if event.matches(message):
                    await callback(message)

            self.handlers.add(wrapper)

            return callback

        return decorator

    def on_command(self, *commands):

        def decorator(callback):

            for command in commands:

                command = command.lstrip("/")

                self.handlers.add(
                    callback,
                    command=command
                )

            return callback

        return decorator

    def on_text(self, text):

        def decorator(callback):

            self.handlers.add(
                callback,
                text=text
            )

            return callback

        return decorator

    async def start(self):

        await self.transport.connect()

        self._running = True

        while self._running:

            updates = await self.transport.updates()

            for raw in updates or []:

                message = self._convert_message(
                    raw
                )

                if message is not None:
                    await self.handlers.dispatch(
                        message
                    )

            await asyncio.sleep(
                self.poll_interval
            )

    async def stop(self):

        self._running = False

        await self.transport.close()

    async def send_message(
        self,
        chat_id,
        text
    ):
        return await self.transport.request(
            "send_message",
            chat_id=chat_id,
            text=text
        )

    async def delete_message(
        self,
        chat_id,
        message_id
    ):
        return await self.transport.request(
            "delete_message",
            chat_id=chat_id,
            message_id=message_id
        )

    async def get_me(self):

        return await self.transport.request(
            "get_me"
        )

    def _convert_message(self, raw):

        if isinstance(raw, Message):

            raw.client = self

            return raw

        if not isinstance(raw, dict):
            return None

        user_data = raw.get(
            "from_user"
        ) or raw.get(
            "sender"
        )

        chat_data = raw.get(
            "chat"
        )

        user = None

        if isinstance(user_data, dict):

            user = User(
                id=user_data.get("id"),
                first_name=user_data.get(
                    "first_name"
                ),
                last_name=user_data.get(
                    "last_name"
                ),
                username=user_data.get(
                    "username"
                ),
                raw=user_data
            )

        chat = None

        if isinstance(chat_data, dict):

            chat = Chat(
                id=chat_data.get("id"),
                type=chat_data.get("type"),
                title=chat_data.get("title"),
                username=chat_data.get(
                    "username"
                ),
                raw=chat_data
            )

        return Message(
            id=raw.get("id"),
            text=raw.get("text"),
            chat=chat,
            from_user=user,
            raw=raw,
            client=self
        )

    def run(self):

        asyncio.run(
            self.start()
        )