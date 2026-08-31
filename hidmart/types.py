from dataclasses import dataclass
from typing import Optional, Any, Dict


# =========================================
# User
# =========================================

@dataclass
class User:
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
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


# =========================================
# Chat
# =========================================

@dataclass
class Chat:
    id: int
    type: Optional[str] = None
    title: Optional[str] = None
    username: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
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
        return self.type in (
            "group",
            "supergroup",
        )


# =========================================
# Message
# =========================================

@dataclass
class Message:
    message_id: int
    chat: Chat

    from_user: Optional[User] = None
    text: Optional[str] = None

    raw: Optional[Dict[str, Any]] = None
    bot: Any = None

    # =====================================
    # Create Message
    # =====================================

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        bot=None,
    ):
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

    # =====================================
    # Basic information
    # =====================================

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

    # =====================================
    # Media
    # =====================================

    @property
    def photo(self):
        if not self.raw:
            return None

        return self.raw.get("photo")

    @property
    def video(self):
        if not self.raw:
            return None

        return self.raw.get("video")

    @property
    def audio(self):
        if not self.raw:
            return None

        return self.raw.get("audio")

    @property
    def document(self):
        if not self.raw:
            return None

        return self.raw.get("document")

    @property
    def voice(self):
        if not self.raw:
            return None

        return self.raw.get("voice")

    @property
    def sticker(self):
        if not self.raw:
            return None

        return self.raw.get("sticker")

    @property
    def location(self):
        if not self.raw:
            return None

        return self.raw.get("location")

    @property
    def contact(self):
        if not self.raw:
            return None

        return self.raw.get("contact")

    # =====================================
    # Media status
    # =====================================

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

    # =====================================
    # Reply message
    # =====================================

    async def reply(
        self,
        text: str,
        **kwargs,
    ):
        return await self.bot.send_message(
            chat_id=self.chat.id,
            text=text,
            **kwargs,
        )

    async def answer(
        self,
        text: str,
        **kwargs,
    ):
        return await self.reply(
            text,
            **kwargs,
        )

    # =====================================
    # Delete message
    # =====================================

    async def delete(self):
        return await self.bot.delete_message(
            chat_id=self.chat.id,
            message_id=self.message_id,
        )

    # =====================================
    # Reply Photo
    # =====================================

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

    # =====================================
    # Reply Video
    # =====================================

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

    # =====================================
    # Reply Audio
    # =====================================

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

    # =====================================
    # Reply Document
    # =====================================

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

    # =====================================
    # Reply Voice
    # =====================================

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

    # =====================================
    # Raw data access
    # =====================================

    def get(
        self,
        key,
        default=None,
    ):
        if not self.raw:
            return default

        return self.raw.get(
            key,
            default,
        )

    def __getitem__(self, key):
        if not self.raw:
            raise KeyError(key)

        return self.raw[key]

    # =====================================
    # String representation
    # =====================================

    def __repr__(self):
        return (
            f"Message("
            f"id={self.message_id}, "
            f"text={self.text!r}, "
            f"chat={self.chat.id}"
            f")"
        )