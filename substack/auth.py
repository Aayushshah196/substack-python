from typing import Dict, Optional, Union

from .errors import AuthenticationError


class SubstackAuth:
    def __init__(self, substack_domain: str):
        self._substack_domain = substack_domain
        self._auth_cookies: Optional[str] = ""
        self._user_details = dict()

    @property
    def cookie(self) -> str:
        return self._auth_cookies

    def get_user_details(self) -> Dict[str, str]:
        return self._user_details

    def set_auth_cookie_manually(self, _auth_cookies: Union[dict, str]) -> None:
        new_auth_cookies = dict()
        if isinstance(_auth_cookies, str):
            new_auth_cookies = self._cookie_str_to_dict(_auth_cookies)
        elif isinstance(_auth_cookies, dict):
            new_auth_cookies = _auth_cookies.copy()
        prev_cookies: dict = self._cookie_str_to_dict(self._auth_cookies)
        prev_cookies.update(new_auth_cookies)
        self._auth_cookies = self._cookie_dict_to_str(prev_cookies)

    def add_session_id_cookie(self, session_id: str) -> None:
        self.set_auth_cookie_manually({"substack.sid": session_id})

    @staticmethod
    def _cookie_dict_to_str(cookie: dict) -> str:
        return "; ".join(f"{key}={value}" for key, value in cookie.items())

    @staticmethod
    def _cookie_str_to_dict(cookie: str) -> dict:
        cookie_list = [kv_pair.split("=") for kv_pair in cookie.split("; ") if kv_pair.strip()]
        return {k: v for k, v in cookie_list if k.strip() and v.strip()}

    def login(self, http_client, email: str, password: str, substack_domain: str = None) -> bool:
        payload = {
            "captcha_response": None,
            "email": email,
            "for_pub": "",
            "password": password,
            "redirect": "/",
        }
        url = "https://substack.com/api/v1/login"
        response = http_client.request("POST", url, data=payload, raw_response=True)
        if "error" in response:
            raise AuthenticationError(response["error"])
        self._auth_cookies = self.set_auth_cookie_manually(response.cookies.get_dict())
        return response

    def get_auth_header(self) -> Dict[str, str]:
        if not self._auth_cookies:
            raise AuthenticationError("No authentication cookie set. Please login or set the cookie manually.")

        return {"Cookie": self._auth_cookies}

    @property
    def is_authenticated(self) -> bool:
        return bool(self._auth_cookies)
