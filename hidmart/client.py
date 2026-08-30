import requests

from .exceptions import APIError, NetworkError


class Client:
    def __init__(self, token: str, base_url: str):
        self.token = token
        self.base_url = base_url.rstrip("/")

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "HidMart/1.0.0"
        })

    def request(self, method: str, data=None):
        url = f"{self.base_url}/{method}"

        try:
            response = self.session.post(
                url,
                json=data or {},
                timeout=30
            )
        except requests.RequestException as error:
            raise NetworkError(str(error)) from error

        try:
            result = response.json()
        except ValueError:
            raise APIError(
                f"Invalid response from Bale API: {response.text}"
            )

        if not response.ok:
            raise APIError(
                result.get("description", "Bale API request failed")
            )

        return result