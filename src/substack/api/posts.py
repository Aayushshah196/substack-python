import base64
import os
from datetime import datetime
from typing import Any, Dict

from loguru import logger

from ..utils.decorators import login_required
from .base import BaseAPI


class PostsAPI(BaseAPI):

    @login_required
    def create_post(self, title: str, content: str) -> Dict[str, Any]:
        url = f"{self.base_url}/posts"
        return self._http_client.request("POST", url, authenticated=True, data={"title": title, "content": content})

    def get_post(self, post_slug: str, **kwargs) -> Dict[str, Any]:
        substack_domain = kwargs.get("substack_domain")
        url = self.build_url(self.base_url(substack_domain), ["posts", post_slug])
        return self._http_client.request("GET", url, authenticated=False)

    @login_required
    def get_all_posts(self, substack_domain: str = None, limit: int = 5) -> Dict[str, Any]:
        base_url = self.base_url(substack_domain)
        query_params = {"limit": limit}
        url = self.build_url(base_url, "posts")
        return self._http_client.request("GET", url, authenticated=True, params=query_params)

    def get_public_posts(self, limit: int = 10, offset: int = 0, sort: str = "top", **kwargs) -> dict:
        """
        Get public posts.

        Args:
            **kwargs:
        """
        substack_domain = kwargs.get("substack_domain")
        url = self.build_url(self.base_url(substack_domain), ["archive"])
        query_params = {"limit": limit, "offset": offset, "sort": "top"}
        response = self._http_client.request("GET", url, authenticated=False, params=query_params)
        return response

    @login_required
    def create_new_post(self, title: str, content: str, **kwargs) -> Dict[str, Any]:
        substack_domain = kwargs.get("substack_domain")
        url = self.build_url(self.base_url(substack_domain), "posts")
        return self._http_client.request("POST", url, authenticated=True, data={"title": title, "content": content})

    @login_required
    def get_post_comments(self, post_id: str, **kwargs) -> Dict[str, Any]:
        substack_domain = kwargs.get("substack_domain")
        url = self.build_url(self.base_url(substack_domain), ["post", post_id, "comments"])
        query_params = {"all_comments": "true"}
        response = self._http_client.request("GET", url, authenticated=True, params=query_params)
        return response

    @login_required
    def create_new_draft(self, draft_content: dict, **kwargs) -> Dict[str, Any]:
        payload = draft_content
        url = self.build_url(self.base_url(), "drafts")
        return self._http_client.request("POST", url, authenticated=True, data=payload)

    @login_required
    def prepublish_draft(self, draft, **kwargs) -> dict:
        """

        Args:
            draft: draft id

        Returns:

        """
        url = self.build_url(
            self.base_url(),
            ["drafts", draft, "prepublish"],
        )
        response = self._http_client.request("GET", url, authenticated=True)
        return response

    @login_required
    def publish_draft(
        self,
        draft_id: str,
        send: bool = True,
        share_automatically: bool = False,
        **kwargs,
    ) -> dict:
        """

        Args:
            draft: draft id
            send:
            share_automatically:
        https://strivewithaayush.substack.com/api/v1/drafts/147559441/publish
        Returns:

        """
        url = self.build_url(
            self.base_url(),
            ["drafts", draft_id, "publish"],
        )
        payload = {"send": send, "share_automatically": share_automatically}
        response = self._http_client.request(
            "POST",
            url,
            authenticated=True,
            data=payload,
        )
        return response

    @login_required
    def schedule_draft(self, draft, draft_datetime: datetime, **kwargs) -> dict:
        """

        Args:
            draft: draft id
            draft_datetime: datetime to schedule the draft

        Returns:

        """
        url = self.build_url(
            self.base_url(),
            ["drafts", draft, "schedule"],
        )
        payload = {"post_date": draft_datetime.isoformat()}
        response = self._http_client.request(
            "POST",
            url,
            authenticated=True,
            data=payload,
        )
        return response

    @login_required
    def unschedule_draft(self, draft, **kwargs) -> dict:
        """

        Args:
            draft: draft id

        Returns:

        """
        url = self.build_url(
            self.base_url(),
            ["drafts", draft, "schedule"],
        )
        payload = {"post_date": None}
        response = self._http_client.request(
            "POST",
            url,
            authenticated=True,
            data=payload,
        )
        return response

    @login_required
    def upload_image(self, image: str):
        """

        This method generates a new substack link that contains the image.

        Args:
            image: filepath or original url of image.

        Returns:

        """
        if not os.path.exists(image):
            raise FileNotFoundError(f"Image not found: {image}")
        with open(image, "rb") as file:
            image = b"data:image/jpeg;base64," + base64.b64encode(file.read())

        url = self.build_url(
            self.base_url(),
            ["publication", "image"],
        )
        payload = {"image": image}
        response = self._http_client.request(
            "POST",
            url,
            authenticated=True,
            data=payload,
        )
        return response

    @login_required
    def get_post_tags(self, post_id: str, **kwargs) -> dict:
        """
        Get tags for post.

        Args:
            post_id: post id
            **kwargs:
        """
        url = self.build_url(self.base_url(), ["post", post_id, "tag"])
        response = self._http_client.request("GET", url, authenticated=True)
        return response
