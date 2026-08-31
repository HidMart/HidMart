import inspect


class Handler:

    def __init__(self, callback):
        self.callback = callback

    async def run(self, message):

        result = self.callback(message)

        if inspect.isawaitable(result):
            await result


class CommandHandler(Handler):

    def __init__(
        self,
        command,
        callback,
    ):

        super().__init__(callback)

        if isinstance(command, str):
            command = [command]

        self.commands = {
            str(item)
            .lstrip("/")
            .lower()
            for item in command
        }

    def matches(self, message):

        if not message.text:
            return False

        text = message.text.strip()

        if not text.startswith("/"):
            return False

        command = text[1:].split()[0].lower()

        return command in self.commands


class MessageHandler(Handler):

    def matches(self, message):

        return bool(message.text)


class TextHandler(Handler):

    def __init__(
        self,
        text,
        callback,
    ):

        super().__init__(callback)

        self.text = text

    def matches(self, message):

        return message.text == self.text


class MediaHandler(Handler):

    def __init__(
        self,
        media_type,
        callback,
    ):

        super().__init__(callback)

        self.media_type = media_type

    def matches(self, message):

        return message.has_media_type(
            self.media_type
        )


class PhotoHandler(MediaHandler):

    def __init__(self, callback):

        super().__init__(
            "photo",
            callback,
        )


class VideoHandler(MediaHandler):

    def __init__(self, callback):

        super().__init__(
            "video",
            callback,
        )


class AudioHandler(MediaHandler):

    def __init__(self, callback):

        super().__init__(
            "audio",
            callback,
        )


class DocumentHandler(MediaHandler):

    def __init__(self, callback):

        super().__init__(
            "document",
            callback,
        )


class VoiceHandler(MediaHandler):

    def __init__(self, callback):

        super().__init__(
            "voice",
            callback,
        )


class StickerHandler(MediaHandler):

    def __init__(self, callback):

        super().__init__(
            "sticker",
            callback,
        )


class LocationHandler(MediaHandler):

    def __init__(self, callback):

        super().__init__(
            "location",
            callback,
        )


class ContactHandler(MediaHandler):

    def __init__(self, callback):

        super().__init__(
            "contact",
            callback,
        )


class MediaAnyHandler(Handler):

    def matches(self, message):

        return message.has_media