from .auth import SubstackAuth
from .utils.http import HTTPClient


class SubstackClient:
    def __init__(self, substack_domain: str):
        self._substack_domain = substack_domain
        self._auth = SubstackAuth(substack_domain)
        self._http_client = HTTPClient(substack_domain, self._auth)

    @property
    def substack_domain(self) -> str:
        return self._substack_domain

    def login(self, email: str, password: str) -> bool:
        return self._auth.login(self._http_client, email, password)

    def set_auth_cookie(self, auth_cookie: str) -> None:
        self._auth.set_auth_cookie_manually(auth_cookie)

    def __repr__(self) -> str:
        return f"SubstackClient(substack_domain={self.substack_domain})"
