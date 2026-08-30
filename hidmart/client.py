import httpx

from .exceptions import APIError, NetworkError


class BaleClient:

    def __init__(
        self,
        token: str,
        base_url: str = "https://tapi.bale.ai"
    ):
        self.token = token
        self.base_url = base_url.rstrip("/")

        self.http = httpx.AsyncClient(
            timeout=30.0
        )

    def _url(self, method: str):
        return f"{self.base_url}/bot{self.token}/{method}"

    async def call(self, method: str, data=None):
        try:
            response = await self.http.post(
                self._url(method),
                json=data or {}
            )

        except httpx.HTTPError as exc:
            raise NetworkError(str(exc)) from exc

        try:
            result = response.json()
        except Exception:
            raise APIError(
                f"Invalid API response: {response.text}"
            )

        if not result.get("ok", False):
            raise APIError(
                description=result.get(
                    "description",
                    "Bale API request failed"
                ),
                error_code=result.get("error_code")
            )

        return result.get("result")

    async def close(self):
        await self.http.aclose()