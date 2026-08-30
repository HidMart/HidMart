from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class User:
    id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@dataclass
class Chat:
    id: int
    type: Optional[str] = None
    title: Optional[str] = None
    username: Optional[str] = None


@dataclass
class Message:
    message_id: int
    chat: Optional[Chat] = None
    from_user: Optional[User] = None
    text: Optional[str] = None
    raw: Optional[dict[str, Any]] = None