import inspect


class Handler:

    def __init__(self, callback):
        self.callback = callback

    async def run(self, message):
        result = self.callback(message)

        if inspect.isawaitable(result):
            await result


class CommandHandler(Handler):

    def __init__(self, command, callback):
        super().__init__(callback)

        self.command = command.lstrip("/").lower()

    def matches(self, message):
        if not message.text:
            return False

        text = message.text.strip()

        if not text.startswith("/"):
            return False

        command = text[1:].split()[0].lower()

        return command == self.command


class MessageHandler(Handler):

    def matches(self, message):
        return bool(message.text)