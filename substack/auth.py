from typing import Dict, Optional

from .errors import AuthenticationError


class SubstackAuth:
    def __init__(self, substack_domain: str):
        self._substack_domain = substack_domain
        self._auth_cookie: Optional[str] = None

    def set_auth_cookie_manually(self, auth_cookie: str) -> None:
        self._auth_cookie = auth_cookie

    def login(self, http_client, email: str, password: str) -> bool:
        payload = {
            "captcha_response": None,
            "email": email,
            "for_pub": "",
            "password": password,
            "redirect": "/",
        }
        url = "https://substack.com/api/v1/login"
        response = http_client.request("POST", url, data=payload)
        if "error" in response:
            raise AuthenticationError(response["error"])
        self._auth_cookie = response["cookie"]
        return True

    def get_auth_header(self) -> Dict[str, str]:
        if not self._auth_cookie:
            raise AuthenticationError("No authentication cookie set. Please login or set the cookie manually.")
        return {"Cookie": self._auth_cookie}

    @property
    def is_authenticated(self) -> bool:
        return self._auth_cookie is not None
