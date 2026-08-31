from dataclasses import dataclass
from typing import Optional, Any, Dict


@dataclass
class User:

    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            username=data.get("username"),
        )

    @property
    def full_name(self):
        parts = []

        if self.first_name:
            parts.append(self.first_name)

        if self.last_name:
            parts.append(self.last_name)

        return " ".join(parts)


@dataclass
class Chat:

    id: int
    type: Optional[str] = None
    title: Optional[str] = None
    username: Optional[str] = None

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            type=data.get("type"),
            title=data.get("title"),
            username=data.get("username"),
        )

    @property
    def is_private(self):
        return self.type == "private"

    @property
    def is_group(self):
        return self.type in ("group", "supergroup")


@dataclass
class Message:

    message_id: int
    chat: Chat

    from_user: Optional[User] = None
    text: Optional[str] = None

    raw: Optional[Dict[str, Any]] = None
    bot: Any = None

    @classmethod
    def from_dict(cls, data, bot=None):

        user_data = data.get("from")
        chat_data = data.get("chat", {})

        return cls(
            message_id=data.get("message_id"),
            chat=Chat.from_dict(chat_data),
            from_user=(
                User.from_dict(user_data)
                if user_data
                else None
            ),
            text=data.get("text"),
            raw=data,
            bot=bot,
        )

    @property
    def id(self):
        return self.message_id

    @property
    def sender(self):
        return self.from_user

    @property
    def caption(self):

        if not self.raw:
            return None

        return self.raw.get("caption")

    # -------------------------
    # Media
    # -------------------------

    @property
    def photo(self):
        return self._media("photo")

    @property
    def video(self):
        return self._media("video")

    @property
    def audio(self):
        return self._media("audio")

    @property
    def document(self):
        return self._media("document")

    @property
    def voice(self):
        return self._media("voice")

    @property
    def sticker(self):
        return self._media("sticker")

    @property
    def location(self):
        return self._media("location")

    @property
    def contact(self):
        return self._media("contact")

    def _media(self, name):

        if not self.raw:
            return None

        return self.raw.get(name)

    @property
    def has_media(self):

        return any([
            self.photo is not None,
            self.video is not None,
            self.audio is not None,
            self.document is not None,
            self.voice is not None,
            self.sticker is not None,
            self.location is not None,
            self.contact is not None,
        ])

    def has_media_type(self, media_type):

        return getattr(
            self,
            media_type,
            None,
        ) is not None

    # -------------------------
    # Replies
    # -------------------------

    async def reply(self, text, **kwargs):

        return await self.bot.send_message(
            self.chat.id,
            text,
            **kwargs,
        )

    async def answer(self, text, **kwargs):

        return await self.reply(
            text,
            **kwargs,
        )

    async def delete(self):

        return await self.bot.delete_message(
            self.chat.id,
            self.message_id,
        )

    async def reply_photo(
        self,
        photo,
        caption=None,
        **kwargs,
    ):

        return await self.bot.send_photo(
            self.chat.id,
            photo,
            caption=caption,
            **kwargs,
        )

    async def reply_video(
        self,
        video,
        caption=None,
        **kwargs,
    ):

        return await self.bot.send_video(
            self.chat.id,
            video,
            caption=caption,
            **kwargs,
        )

    async def reply_audio(
        self,
        audio,
        caption=None,
        **kwargs,
    ):

        return await self.bot.send_audio(
            self.chat.id,
            audio,
            caption=caption,
            **kwargs,
        )

    async def reply_document(
        self,
        document,
        caption=None,
        **kwargs,
    ):

        return await self.bot.send_document(
            self.chat.id,
            document,
            caption=caption,
            **kwargs,
        )

    async def reply_voice(
        self,
        voice,
        caption=None,
        **kwargs,
    ):

        return await self.bot.send_voice(
            self.chat.id,
            voice,
            caption=caption,
            **kwargs,
        )

    # -------------------------
    # Raw
    # -------------------------

    def get(self, key, default=None):

        if not self.raw:
            return default

        return self.raw.get(key, default)

    def __getitem__(self, key):

        if not self.raw:
            raise KeyError(key)

        return self.raw[key]

    def __repr__(self):

        return (
            f"Message("
            f"id={self.message_id}, "
            f"text={self.text!r}, "
            f"chat={self.chat.id}"
            f")"
        )