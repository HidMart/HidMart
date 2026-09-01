from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from .exceptions import (
    APIError,
    NetworkError,
    InvalidTokenError,
)


class Client:
    """
    Internal asynchronous HTTP client for the Bale Bot API.
    """

    def __init__(
        self,
        token: str,
        *,
        timeout: float = 30.0,
    ):
        if not token:
            raise InvalidTokenError("Bot token is required")

        self.token = token
        self.timeout = timeout

        self.base_url = (
            f"https://tapi.bale.ai/bot{self.token}"
        )

        self._client: Optional[httpx.AsyncClient] = None

    # =========================
    # Lifecycle
    # =========================

    async def start(self):
        """Create the HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.timeout
            )

    async def close(self):
        """Close the HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        await self.close()

    # =========================
    # Request
    # =========================

    async def request(
        self,
        method: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Send a POST request to the Bale Bot API.
        """

        if self._client is None:
            await self.start()

        url = f"{self.base_url}/{method}"

        try:
            response = await self._client.post(
                url,
                json=data or {},
            )

        except httpx.HTTPError as exc:
            raise NetworkError(
                f"Network error: {exc}"
            ) from exc

        if response.status_code == 401:
            raise InvalidTokenError(
                "Invalid bot token"
            )

        try:
            result = response.json()

        except ValueError as exc:
            raise APIError(
                "Invalid JSON response from Bale API"
            ) from exc

        if not result.get("ok", False):
            description = result.get(
                "description",
                "Unknown API error",
            )

            raise APIError(description)

        return result.get("result")

    async def call(
        self,
        method: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Alias for request().
        """

        return await self.request(
            method,
            data,
        )

    # =========================
    # Information
    # =========================

    async def get_me(self):
        return await self.call(
            "getMe"
        )

    async def get_chat(
        self,
        chat_id,
    ):
        return await self.call(
            "getChat",
            {
                "chat_id": chat_id,
            },
        )

    async def get_chat_member(
        self,
        chat_id,
        user_id,
    ):
        return await self.call(
            "getChatMember",
            {
                "chat_id": chat_id,
                "user_id": user_id,
            },
        )

    # =========================
    # Updates
    # =========================

    async def get_updates(
        self,
        *,
        offset=None,
        limit=None,
        timeout=None,
    ):
        data = {}

        if offset is not None:
            data["offset"] = offset

        if limit is not None:
            data["limit"] = limit

        if timeout is not None:
            data["timeout"] = timeout

        return await self.call(
            "getUpdates",
            data,
        )

    # =========================
    # Sending
    # =========================

    async def send_message(
        self,
        chat_id,
        text,
        *,
        reply_markup=None,
        **kwargs,
    ):
        data = {
            "chat_id": chat_id,
            "text": text,
        }

        if reply_markup is not None:
            data["reply_markup"] = reply_markup

        data.update(kwargs)

        return await self.call(
            "sendMessage",
            data,
        )

    async def send_photo(
        self,
        chat_id,
        photo,
        *,
        caption=None,
        reply_markup=None,
        **kwargs,
    ):
        data = {
            "chat_id": chat_id,
            "photo": photo,
        }

        if caption is not None:
            data["caption"] = caption

        if reply_markup is not None:
            data["reply_markup"] = reply_markup

        data.update(kwargs)

        return await self.call(
            "sendPhoto",
            data,
        )

    async def send_video(
        self,
        chat_id,
        video,
        *,
        caption=None,
        reply_markup=None,
        **kwargs,
    ):
        data = {
            "chat_id": chat_id,
            "video": video,
        }

        if caption is not None:
            data["caption"] = caption

        if reply_markup is not None:
            data["reply_markup"] = reply_markup

        data.update(kwargs)

        return await self.call(
            "sendVideo",
            data,
        )

    async def send_audio(
        self,
        chat_id,
        audio,
        *,
        caption=None,
        reply_markup=None,
        **kwargs,
    ):
        data = {
            "chat_id": chat_id,
            "audio": audio,
        }

        if caption is not None:
            data["caption"] = caption

        if reply_markup is not None:
            data["reply_markup"] = reply_markup

        data.update(kwargs)

        return await self.call(
            "sendAudio",
            data,
        )

    async def send_document(
        self,
        chat_id,
        document,
        *,
        caption=None,
        reply_markup=None,
        **kwargs,
    ):
        data = {
            "chat_id": chat_id,
            "document": document,
        }

        if caption is not None:
            data["caption"] = caption

        if reply_markup is not None:
            data["reply_markup"] = reply_markup

        data.update(kwargs)

        return await self.call(
            "sendDocument",
            data,
        )

    async def send_voice(
        self,
        chat_id,
        voice,
        *,
        caption=None,
        reply_markup=None,
        **kwargs,
    ):
        data = {
            "chat_id": chat_id,
            "voice": voice,
        }

        if caption is not None:
            data["caption"] = caption

        if reply_markup is not None:
            data["reply_markup"] = reply_markup

        data.update(kwargs)

        return await self.call(
            "sendVoice",
            data,
        )

    async def send_location(
        self,
        chat_id,
        latitude,
        longitude,
        *,
        reply_markup=None,
        **kwargs,
    ):
        data = {
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude,
        }

        if reply_markup is not None:
            data["reply_markup"] = reply_markup

        data.update(kwargs)

        return await self.call(
            "sendLocation",
            data,
        )

    # =========================
    # Message management
    # =========================

    async def edit_message_text(
        self,
        chat_id,
        message_id,
        text,
        *,
        reply_markup=None,
        **kwargs,
    ):
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
        }

        if reply_markup is not None:
            data["reply_markup"] = reply_markup

        data.update(kwargs)

        return await self.call(
            "editMessageText",
            data,
        )

    async def delete_message(
        self,
        chat_id,
        message_id,
    ):
        return await self.call(
            "deleteMessage",
            {
                "chat_id": chat_id,
                "message_id": message_id,
            },
        )


# ==========================================
# Backward/internal compatibility
# ==========================================

BaleClient = Client