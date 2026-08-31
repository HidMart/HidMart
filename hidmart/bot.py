import asyncio
import logging

from .client import BaleClient
from .types import Message

from .handlers import (
    CommandHandler,
    MessageHandler,
    TextHandler,
    PhotoHandler,
    VideoHandler,
    AudioHandler,
    DocumentHandler,
    VoiceHandler,
    StickerHandler,
    LocationHandler,
    ContactHandler,
    MediaAnyHandler,
)


logger = logging.getLogger("hidmart")


class Bot:

    def __init__(
        self,
        token,
        poll_interval=1.0,
        timeout=25,
    ):

        if not token:
            raise ValueError(
                "Bot token is required"
            )

        self.token = token
        self.poll_interval = poll_interval
        self.timeout = timeout

        self.client = BaleClient(token)

        self.handlers = []

        self.running = False
        self.offset = None
        self.me = None

    # =====================================
    # HANDLERS
    # =====================================

    def on_command(self, *commands):

        if not commands:
            raise ValueError(
                "At least one command is required"
            )

        def decorator(callback):

            self.handlers.append(
                CommandHandler(
                    commands,
                    callback,
                )
            )

            return callback

        return decorator

    def on_message(self):

        def decorator(callback):

            self.handlers.append(
                MessageHandler(callback)
            )

            return callback

        return decorator

    def on_text(self, text):

        def decorator(callback):

            self.handlers.append(
                TextHandler(
                    text,
                    callback,
                )
            )

            return callback

        return decorator

    def on_photo(self):

        def decorator(callback):

            self.handlers.append(
                PhotoHandler(callback)
            )

            return callback

        return decorator

    def on_video(self):

        def decorator(callback):

            self.handlers.append(
                VideoHandler(callback)
            )

            return callback

        return decorator

    def on_audio(self):

        def decorator(callback):

            self.handlers.append(
                AudioHandler(callback)
            )

            return callback

        return decorator

    def on_document(self):

        def decorator(callback):

            self.handlers.append(
                DocumentHandler(callback)
            )

            return callback

        return decorator

    def on_voice(self):

        def decorator(callback):

            self.handlers.append(
                VoiceHandler(callback)
            )

            return callback

        return decorator

    def on_sticker(self):

        def decorator(callback):

            self.handlers.append(
                StickerHandler(callback)
            )

            return callback

        return decorator

    def on_location(self):

        def decorator(callback):

            self.handlers.append(
                LocationHandler(callback)
            )

            return callback

        return decorator

    def on_contact(self):

        def decorator(callback):

            self.handlers.append(
                ContactHandler(callback)
            )

            return callback

        return decorator

    def on_media(self):

        def decorator(callback):

            self.handlers.append(
                MediaAnyHandler(callback)
            )

            return callback

        return decorator

    # =====================================
    # SEND
    # =====================================

    async def send_message(
        self,
        chat_id,
        text,
        **kwargs,
    ):

        return await self.client.send_message(
            chat_id,
            text,
            **kwargs,
        )

    async def send_photo(
        self,
        chat_id,
        photo,
        caption=None,
        **kwargs,
    ):

        return await self.client.send_photo(
            chat_id,
            photo,
            caption,
            **kwargs,
        )

    async def send_video(
        self,
        chat_id,
        video,
        caption=None,
        **kwargs,
    ):

        return await self.client.send_video(
            chat_id,
            video,
            caption,
            **kwargs,
        )

    async def send_audio(
        self,
        chat_id,
        audio,
        caption=None,
        **kwargs,
    ):

        return await self.client.send_audio(
            chat_id,
            audio,
            caption,
            **kwargs,
        )

    async def send_document(
        self,
        chat_id,
        document,
        caption=None,
        **kwargs,
    ):

        return await self.client.send_document(
            chat_id,
            document,
            caption,
            **kwargs,
        )

    async def send_voice(
        self,
        chat_id,
        voice,
        caption=None,
        **kwargs,
    ):

        return await self.client.send_voice(
            chat_id,
            voice,
            caption,
            **kwargs,
        )

    async def send_location(
        self,
        chat_id,
        latitude,
        longitude,
        **kwargs,
    ):

        return await self.client.send_location(
            chat_id,
            latitude,
            longitude,
            **kwargs,
        )

    # =====================================
    # MESSAGE MANAGEMENT
    # =====================================

    async def edit_message_text(
        self,
        chat_id,
        message_id,
        text,
        **kwargs,
    ):

        return await self.client.edit_message_text(
            chat_id,
            message_id,
            text,
            **kwargs,
        )

    async def delete_message(
        self,
        chat_id,
        message_id,
    ):

        return await self.client.delete_message(
            chat_id,
            message_id,
        )

    # =====================================
    # INFORMATION
    # =====================================

    async def get_me(self):

        self.me = await self.client.get_me()

        return self.me

    async def get_chat(self, chat_id):

        return await self.client.get_chat(
            chat_id
        )

    async def get_chat_member(
        self,
        chat_id,
        user_id,
    ):

        return await self.client.get_chat_member(
            chat_id,
            user_id,
        )

    async def get_updates(
        self,
        offset=None,
        timeout=None,
        limit=None,
    ):

        if timeout is None:
            timeout = self.timeout

        return await self.client.get_updates(
            offset=offset,
            timeout=timeout,
            limit=limit,
        )

    # =====================================
    # UPDATE
    # =====================================

    async def process_update(self, update):

        if not isinstance(update, dict):
            return

        message_data = update.get("message")

        if not message_data:
            return

        message = Message.from_dict(
            message_data,
            bot=self,
        )

        for handler in self.handlers:

            try:

                if hasattr(handler, "matches"):

                    if not handler.matches(message):
                        continue

                await handler.run(message)

            except Exception:

                logger.exception(
                    "Handler error"
                )

    # =====================================
    # START
    # =====================================

    async def start(self):

        self.running = True

        self.me = await self.get_me()

        logger.info(
            "Bot started: %s",
            self.me,
        )

        await self.polling()

    # =====================================
    # POLLING
    # =====================================

    async def polling(self):

        self.running = True

        logger.info(
            "HidMart polling started"
        )

        while self.running:

            try:

                updates = await self.get_updates(
                    offset=self.offset,
                )

                if not updates:

                    await asyncio.sleep(
                        self.poll_interval
                    )

                    continue

                for update in updates:

                    update_id = update.get(
                        "update_id"
                    )

                    if update_id is not None:

                        self.offset = (
                            update_id + 1
                        )

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

        logger.info(
            "HidMart polling stopped"
        )

    # =====================================
    # STOP
    # =====================================

    async def stop(self):

        self.running = False

        await self.client.close()

    # =====================================
    # RUN
    # =====================================

    async def _run(self):

        try:

            await self.start()

        finally:

            await self.client.close()

    def run(self):

        try:

            asyncio.run(
                self._run()
            )

        except KeyboardInterrupt:

            logger.info(
                "HidMart stopped by user"
            )