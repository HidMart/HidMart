from __future__ import annotations

import json
import os
from pathlib import Path

from .errors import SessionError


class Session:

    def __init__(self, path="hidmart.session.json"):
        self.path = Path(path)

        self.access_token = None
        self.user_id = None
        self.user_name = None

    @property
    def authorized(self):
        return bool(self.access_token)

    def set(
        self,
        access_token,
        user_id=None,
        user_name=None,
    ):
        access_token = str(access_token).strip()

        if not access_token:
            raise SessionError(
                "access token is empty"
            )

        self.access_token = access_token
        self.user_id = user_id
        self.user_name = user_name

    def save(self):

        if not self.access_token:
            raise SessionError(
                "cannot save empty session"
            )

        data = {
            "version": 1,
            "access_token": self.access_token,
            "user_id": self.user_id,
            "user_name": self.user_name,
        }

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        tmp = self.path.with_suffix(
            self.path.suffix + ".tmp"
        )

        try:
            tmp.write_text(
                json.dumps(
                    data,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            os.replace(
                tmp,
                self.path,
            )

            try:
                os.chmod(
                    self.path,
                    0o600,
                )
            except OSError:
                pass

        except OSError as exc:
            raise SessionError(
                str(exc)
            ) from exc

    def load(self):

        if not self.path.exists():
            return False

        try:
            data = json.loads(
                self.path.read_text(
                    encoding="utf-8"
                )
            )
        except (
            OSError,
            json.JSONDecodeError,
        ) as exc:
            raise SessionError(
                f"invalid session: {exc}"
            ) from exc

        token = data.get(
            "access_token"
        )

        if not token:
            return False

        self.access_token = token
        self.user_id = data.get(
            "user_id"
        )
        self.user_name = data.get(
            "user_name"
        )

        return True

    def clear(self):

        self.access_token = None
        self.user_id = None
        self.user_name = None

        try:
            self.path.unlink(
                missing_ok=True
            )
        except OSError as exc:
            raise SessionError(
                str(exc)
            ) from exc