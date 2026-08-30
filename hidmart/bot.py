import asyncio
import logging

from .client import BaleClient
from .types import Message
from .handlers import CommandHandler, MessageHandler


logger = logging.getLogger("hidmart")


class Bot:

    def __init__(
        self,
        token: str,
        poll_interval: float = 1.0
    ):
        if not token:
            raise ValueError("Bot token is required")

        self.token = token
        self.poll_interval = poll_interval

        self.client = BaleClient(token)

        self.handlers = []

        self.running = False
        self.offset = None

    def on_command(self, command):

        def decorator(callback):
            handler = CommandHandler(
                command,
                callback
            )

            self.handlers.append(handler)

            return callback

        return decorator

    def on_message(self):

        def decorator(callback):
            handler = MessageHandler(callback)

            self.handlers.append(handler)

            return callback

        return decorator

    async def send_message(
        self,
        chat_id,
        text
    ):
        return await self.client.call(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": text
            }
        )

    async def get_me(self):
        return await self.client.call(
            "getMe"
        )

    async def get_updates(
        self,
        offset=None,
        timeout=25
    ):
        data = {
            "timeout": timeout
        }

        if offset is not None:
            data["offset"] = offset

        return await self.client.call(
            "getUpdates",
            data
        )

    async def process_update(self, update):
        if not isinstance(update, dict):
            return

        message_data = update.get("message")

        if not message_data:
            return

        message = Message.from_dict(
            message_data,
            bot=self
        )

        for handler in self.handlers:

            try:

                if hasattr(handler, "matches"):
                    if not handler.matches(message):
                        continue

                await handler.run(message)

            except Exception:
                logger.exception(
                    "Error while processing update"
                )

    async def polling(self):
        self.running = True

        logger.info("HidMart polling started")

        while self.running:

            try:

                updates = await self.get_updates(
                    offset=self.offset,
                    timeout=25
                )

                if not updates:
                    await asyncio.sleep(
                        self.poll_interval
                    )
                    continue

                for update in updates:

                    update_id = update.get("update_id")

                    if update_id is not None:
                        self.offset = update_id + 1

                    await self.process_update(
                        update
                    )

            except asyncio.CancelledError:
                break

            except Exception:
                logger.exception(
                    "Polling error"
                )

                await asyncio.sleep(3)

        logger.info("HidMart polling stopped")

    def run(self):
        try:
            asyncio.run(
                self._run()
            )

        except KeyboardInterrupt:
            logger.info(
                "HidMart stopped by user"
            )

    async def _run(self):

        try:
            me = await self.get_me()

            logger.info(
                "Bot started: %s",
                me
            )

            await self.polling()

        finally:
            await self.client.close()

    def stop(self):
        self.running = False