from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


@dataclass(slots=True)
class User:

    id: int

    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @property
    def full_name(self):

        return " ".join(
            x
            for x in (
                self.first_name,
                self.last_name,
            )
            if x
        )


@dataclass(slots=True)
class Chat:

    id: str

    title: Optional[str] = None
    username: Optional[str] = None
    type: str = "unknown"


@dataclass(slots=True)
class Message:

    id: int
    chat_id: str

    text: str = ""

    sender_id: Optional[int] = None

    date: Optional[datetime] = None

    outgoing: bool = False

    raw: Any = None

    client: Any = None

    async def reply(
        self,
        text: str,
    ):

        if self.client is None:
            raise RuntimeError(
                "Message has no client"
            )

        return await self.client.send_message(
            self.chat_id,
            text,
            reply_to=self.id,
        )

    async def edit(
        self,
        text: str,
    ):

        if self.client is None:
            raise RuntimeError(
                "Message has no client"
            )

        return await self.client.edit_message(
            self.chat_id,
            self.id,
            text,
        )

    async def delete(self):

        if self.client is None:
            raise RuntimeError(
                "Message has no client"
            )

        return await self.client.delete_message(
            self.chat_id,
            self.id,
        )


@dataclass(slots=True)
class Update:

    type: str
    data: Any
    raw: bytes | None = None