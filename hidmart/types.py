from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class User:
    id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            id=str(data.get("id", "")),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            username=data.get("username"),
        )


@dataclass
class Message:
    id: str
    text: Optional[str] = None
    chat_id: Optional[str] = None
    sender_id: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            id=str(data.get("id", "")),
            text=data.get("text"),
            chat_id=str(data["chat_id"]) if data.get("chat_id") else None,
            sender_id=str(data["sender_id"]) if data.get("sender_id") else None,
            raw=data,
        )


@dataclass
class Chat:
    id: str
    title: Optional[str] = None
    chat_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            id=str(data.get("id", "")),
            title=data.get("title"),
            chat_type=data.get("type"),
        )