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
        data = data or {}

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
        data = data or {}

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
        data = data or {}

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

    # ==================================
    # MEDIA DATA
    # ==================================

    @property
    def photo(self):
        return self._get_media("photo")

    @property
    def video(self):
        return self._get_media("video")

    @property
    def audio(self):
        return self._get_media("audio")

    @property
    def document(self):
        return self._get_media("document")

    @property
    def voice(self):
        return self._get_media("voice")

    @property
    def sticker(self):
        return self._get_media("sticker")

    @property
    def location(self):
        return self._get_media("location")

    @property
    def contact(self):
        return self._get_media("contact")

    def _get_media(self, media_type):

        if not self.raw:
            return None

        return self.raw.get(media_type)

    # ==================================
    # FILE ID
    # ==================================

    @staticmethod
    def _extract_file_id(value):

        if value is None:
            return None

        if isinstance(value, str):
            return value

        if isinstance(value, dict):

            for key in (
                "file_id",
                "id",
                "fileId",
                "fileID",
            ):
                if value.get(key):
                    return value[key]

            return None

        return None

    def get_file_id(self, media_type):

        media = self._get_media(media_type)

        # معمولاً photo به صورت list می‌آید
        if isinstance(media, list):

            if not media:
                return None

            # بزرگ‌ترین/آخرین نسخه عکس
            for item in reversed(media):

                file_id = self._extract_file_id(item)

                if file_id:
                    return file_id

            return None

        return self._extract_file_id(media)

    @property
    def photo_id(self):
        return self.get_file_id("photo")

    @property
    def video_id(self):
        return self.get_file_id("video")

    @property
    def audio_id(self):
        return self.get_file_id("audio")

    @property
    def document_id(self):
        return self.get_file_id("document")

    @property
    def voice_id(self):
        return self.get_file_id("voice")

    @property
    def sticker_id(self):
        return self.get_file_id("sticker")

    # ==================================
    # MEDIA CHECK
    # ==================================

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

    # ==================================
    # REPLY
    # ==================================

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

    # ==================================
    # MEDIA REPLY
    # ==================================

    async def reply_photo(
        self,
        photo=None,
        caption=None,
        **kwargs,
    ):

        if photo is None:
            photo = self.photo_id

        if photo is None:
            raise ValueError(
                "Photo file_id was not found"
            )

        return await self.bot.send_photo(
            self.chat.id,
            photo,
            caption=caption,
            **kwargs,
        )

    async def reply_video(
        self,
        video=None,
        caption=None,
        **kwargs,
    ):

        if video is None:
            video = self.video_id

        if video is None:
            raise ValueError(
                "Video file_id was not found"
            )

        return await self.bot.send_video(
            self.chat.id,
            video,
            caption=caption,
            **kwargs,
        )

    async def reply_audio(
        self,
        audio=None,
        caption=None,
        **kwargs,
    ):

        if audio is None:
            audio = self.audio_id

        if audio is None:
            raise ValueError(
                "Audio file_id was not found"
            )

        return await self.bot.send_audio(
            self.chat.id,
            audio,
            caption=caption,
            **kwargs,
        )

    async def reply_document(
        self,
        document=None,
        caption=None,
        **kwargs,
    ):

        if document is None:
            document = self.document_id

        if document is None:
            raise ValueError(
                "Document file_id was not found"
            )

        return await self.bot.send_document(
            self.chat.id,
            document,
            caption=caption,
            **kwargs,
        )

    async def reply_voice(
        self,
        voice=None,
        caption=None,
        **kwargs,
    ):

        if voice is None:
            voice = self.voice_id

        if voice is None:
            raise ValueError(
                "Voice file_id was not found"
            )

        return await self.bot.send_voice(
            self.chat.id,
            voice,
            caption=caption,
            **kwargs,
        )

    # ==================================
    # RAW DATA
    # ==================================

    def get(self, key, default=None):

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

    def __repr__(self):

        return (
            f"Message("
            f"id={self.message_id}, "
            f"text={self.text!r}, "
            f"chat={self.chat.id}"
            f")"
        )