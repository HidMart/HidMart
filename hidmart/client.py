import asyncio
from typing import Any, Dict, Optional

import httpx

from .exceptions import (
    APIError,
    NetworkError,
    InvalidTokenError,
)


class BaleClient:

    def __init__(
        self,
        token: str,
        base_url: str = "https://tapi.bale.ai",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):

        if not token:
            raise ValueError(
                "Bot token is required"
            )

        self.token = token
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

        self.http = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout)
        )

    def _url(self, method):

        return (
            f"{self.base_url}/bot"
            f"{self.token}/{method}"
        )

    async def call(
        self,
        method,
        data: Optional[Dict[str, Any]] = None,
    ):

        payload = data or {}
        last_error = None

        for attempt in range(
            self.max_retries + 1
        ):

            try:

                response = await self.http.post(
                    self._url(method),
                    json=payload,
                )

                response.raise_for_status()

                try:
                    result = response.json()

                except ValueError as exc:

                    raise APIError(
                        "Invalid JSON response"
                    ) from exc

                if not result.get("ok", False):

                    error_code = result.get(
                        "error_code"
                    )

                    description = result.get(
                        "description",
                        "Bale API request failed",
                    )

                    if error_code == 401:

                        raise InvalidTokenError(
                            description
                        )

                    raise APIError(
                        description=description,
                        error_code=error_code,
                    )

                return result.get("result")

            except InvalidTokenError:
                raise

            except APIError:
                raise

            except httpx.HTTPStatusError as exc:

                last_error = exc

                if attempt >= self.max_retries:

                    raise NetworkError(
                        f"HTTP error: "
                        f"{exc.response.status_code}"
                    ) from exc

            except httpx.RequestError as exc:

                last_error = exc

                if attempt >= self.max_retries:

                    raise NetworkError(
                        f"Network error: {exc}"
                    ) from exc

            except httpx.HTTPError as exc:

                last_error = exc

                if attempt >= self.max_retries:

                    raise NetworkError(
                        f"HTTP error: {exc}"
                    ) from exc

            if attempt < self.max_retries:

                await asyncio.sleep(
                    2 ** attempt
                )

        raise NetworkError(
            f"Request failed: {last_error}"
        )

    # ==================================
    # INFORMATION
    # ==================================

    async def get_me(self):

        return await self.call(
            "getMe"
        )

    async def get_updates(
        self,
        offset=None,
        timeout=25,
        limit=None,
    ):

        data = {
            "timeout": timeout
        }

        if offset is not None:
            data["offset"] = offset

        if limit is not None:
            data["limit"] = limit

        return await self.call(
            "getUpdates",
            data,
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

    # ==================================
    # SEND MESSAGE
    # ==================================

    async def send_message(
        self,
        chat_id,
        text,
        **kwargs,
    ):

        data = {
            "chat_id": chat_id,
            "text": text,
        }

        data.update(kwargs)

        return await self.call(
            "sendMessage",
            data,
        )

    # ==================================
    # MEDIA
    # ==================================

    async def send_photo(
        self,
        chat_id,
        photo,
        caption=None,
        **kwargs,
    ):

        data = {
            "chat_id": chat_id,
            "photo": photo,
        }

        if caption is not None:
            data["caption"] = caption

        data.update(kwargs)

        return await self.call(
            "sendPhoto",
            data,
        )

    async def send_video(
        self,
        chat_id,
        video,
        caption=None,
        **kwargs,
    ):

        data = {
            "chat_id": chat_id,
            "video": video,
        }

        if caption is not None:
            data["caption"] = caption

        data.update(kwargs)

        return await self.call(
            "sendVideo",
            data,
        )

    async def send_audio(
        self,
        chat_id,
        audio,
        caption=None,
        **kwargs,
    ):

        data = {
            "chat_id": chat_id,
            "audio": audio,
        }

        if caption is not None:
            data["caption"] = caption

        data.update(kwargs)

        return await self.call(
            "sendAudio",
            data,
        )

    async def send_document(
        self,
        chat_id,
        document,
        caption=None,
        **kwargs,
    ):

        data = {
            "chat_id": chat_id,
            "document": document,
        }

        if caption is not None:
            data["caption"] = caption

        data.update(kwargs)

        return await self.call(
            "sendDocument",
            data,
        )

    async def send_voice(
        self,
        chat_id,
        voice,
        caption=None,
        **kwargs,
    ):

        data = {
            "chat_id": chat_id,
            "voice": voice,
        }

        if caption is not None:
            data["caption"] = caption

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
        **kwargs,
    ):

        data = {
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude,
        }

        data.update(kwargs)

        return await self.call(
            "sendLocation",
            data,
        )

    # ==================================
    # MESSAGE MANAGEMENT
    # ==================================

    async def edit_message_text(
        self,
        chat_id,
        message_id,
        text,
        **kwargs,
    ):

        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
        }

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

    async def close(self):

        await self.http.aclose()