from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class SelfBotUser:
    id: int
    first_name: str = ""
    last_name: str = ""
    username: str = ""

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


@dataclass
class SelfBotChat:
    id: int
    type: str = ""
    title: str = ""
    username: str = ""

    @property
    def is_private(self):
        return self.type == "private"

    @property
    def is_group(self):
        return self.type in ("group", "supergroup")


@dataclass
class SelfBotMessage:
    id: int
    text: str = ""
    chat: Optional[SelfBotChat] = None
    from_user: Optional[SelfBotUser] = None
    raw: Any = None