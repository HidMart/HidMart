from dataclasses import dataclass
from typing import Optional, Any, Dict


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


@dataclass
class Message:
    message_id: int
    chat: Chat
    from_user: Optional[User] = None
    text: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None
    bot: Any = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any], bot=None):
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

    async def reply(self, text: str):
        return await self.bot.send_message(
            chat_id=self.chat.id,
            text=text
        )