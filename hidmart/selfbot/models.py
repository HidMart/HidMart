class User:

    def __init__(
        self,
        id=None,
        first_name=None,
        last_name=None,
        username=None,
        raw=None
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.raw = raw

    @property
    def full_name(self):
        return " ".join(
            x for x in [
                self.first_name,
                self.last_name
            ] if x
        ).strip()


class Chat:

    def __init__(
        self,
        id=None,
        type=None,
        title=None,
        username=None,
        raw=None
    ):
        self.id = id
        self.type = type
        self.title = title
        self.username = username
        self.raw = raw

    @property
    def is_private(self):
        return self.type == "private"

    @property
    def is_group(self):
        return self.type in (
            "group",
            "supergroup"
        )


class Message:

    def __init__(
        self,
        id=None,
        text=None,
        chat=None,
        from_user=None,
        raw=None,
        client=None
    ):
        self.id = id
        self.text = text
        self.chat = chat
        self.from_user = from_user
        self.sender = from_user
        self.raw = raw
        self.client = client

    async def reply(self, text):
        if self.client is None:
            raise RuntimeError(
                "Message is not attached to a client."
            )

        if self.chat is None:
            raise RuntimeError(
                "Message has no chat."
            )

        return await self.client.send_message(
            self.chat.id,
            text
        )

    async def answer(self, text):
        return await self.reply(text)

    async def delete(self):
        if self.client is None:
            raise RuntimeError(
                "Message is not attached to a client."
            )

        return await self.client.delete_message(
            self.chat.id,
            self.id
        )