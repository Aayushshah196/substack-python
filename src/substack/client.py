from typing import Any, Dict

from .api.posts import PostsAPI
from .api.publication import PublicationsAPI
from .api.user import UserAPI
from .auth import SubstackAuth
from .structures import Draft
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

    def create_post(self, draft: Draft) -> Dict[str, Any]:
        draft_res = self.posts.create_post(draft)
        if not draft_res:
            raise Exception("Failed to create post draft")
        draft_id = draft_res.get("id")
        if not draft_id:
            raise Exception("Illegal draft id")
        post_res = self.posts.publish_draft(draft_id)
        return post_res
