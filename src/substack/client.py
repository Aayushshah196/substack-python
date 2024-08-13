from .api.posts import PostsAPI
from .api.publication import PublicationsAPI
from .api.user import UserAPI
from .auth import SubstackAuth
from .utils.http import HTTPClient


class SubstackClient:
    def __init__(self, substack_domain: str):
        self._substack_domain = substack_domain
        self._auth = SubstackAuth(substack_domain)
        self._http_client = HTTPClient(substack_domain, self._auth)
        self.posts: PostsAPI = PostsAPI(self._http_client, self._substack_domain)
        self.publications: PublicationsAPI = PublicationsAPI(self._http_client, self._substack_domain)
        self.user: UserAPI = UserAPI(self._http_client, self._substack_domain)

    @property
    def substack_domain(self) -> str:
        return self._substack_domain

    def login(self, email: str, password: str) -> bool:
        return self._auth.login(self._http_client, email, password, self._substack_domain)

    def set_auth_cookie(self, auth_cookie: str) -> None:
        self._auth.set_auth_cookie_manually(auth_cookie)

    def __repr__(self) -> str:
        return f"SubstackClient(substack_domain={self.substack_domain})"
