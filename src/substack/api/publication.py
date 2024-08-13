from datetime import datetime
from typing import Any, Dict

from ..utils.decorators import login_required
from .base import BaseAPI


class PublicationsAPI(BaseAPI):
    def get_info(self) -> Dict[str, Any]:
        url = f"{self.base_url}/publication"
        return self._http_client.request("GET", url, authenticated=False)

    @login_required
    def get_publication_users(self, substack_domain: str = None) -> Dict[str, Any]:
        """
        Get list of users.

        Returns:

        """
        url = self.build_url(self.base_url(substack_domain), ["publication", "users"])
        response = self._http_client.request("GET", url, authenticated=True)
        return response

    @login_required
    def get_publication_summary(self, substack_domain: str = None) -> Dict[str, Any]:
        """
        Get publication summary.
        Returns:
        """
        url = self.build_url(self.base_url(substack_domain), ["publish-dashboard", "summary"])
        response = self._http_client.request("GET", url, authenticated=False)

        return response

    @login_required
    def get_posts_count(self, **kwargs) -> Dict[str, Any]:
        """
        Get posts count by status
        Returns:
        """
        ""
        url = self.build_url(self.base_url(), ["post_management", "counts"])
        response = self._http_client.request("GET", url, authenticated=True)
        return response

    @login_required
    def get_publication_subscribers_count(self, substack_domain: str = None) -> Dict[str, Any]:
        """
        Get subscriber count.
        Returns:
        """
        url = self.build_url(self.base_url(substack_domain), ["publication_launch_checklist"])
        response = self._http_client.request("GET", url, authenticated=True)
        return response

    def get_published_posts(self, offset=0, limit=25, order_by="post_date", order_direction="desc", **kwargs):
        """
        Get list of published posts for the publication.
        """
        substack_domain = kwargs.get("substack_domain")
        url = self.build_url(self.base_url(substack_domain), ["post_management", "published"])
        query_params = {
            "offset": offset,
            "limit": limit,
            "order_by": order_by,
            "order_direction": order_direction,
        }
        response = self._http_client.request("GET", url, authenticated=True, params=query_params)
        return response

    @login_required
    def get_drafts(self, filter=None, offset=None, limit=None, **kwargs):
        """

        Args:
            filter:
            offset:
            limit:

        Returns:

        """
        substack_domain = kwargs.get("substack_domain")
        url = self.build_url(self.base_url(substack_domain), ["publication", "drafts"])
        query_params = {"filter": filter, "offset": offset, "limit": limit}
        response = self._http_client.request("GET", url, authenticated=True, params=query_params)
        return response

    @login_required
    def get_scheduled_posts(
        self,
        limit: int = 1,
        offset: int = 0,
        order_by: str = "trigger_at",
        order_direction: str = "asc",
    ):
        """
        Get list of scheduled posts for the publication.
        """
        url = self.build_url(self.base_url(), ["post_management", "scheduled"])
        query_params = {
            "offset": offset,
            "limit": limit,
            "order_by": order_by,
            "order_direction": order_direction,
        }
        response = self._http_client.request("GET", url, authenticated=True, params=query_params)
        return response

    @login_required
    def get_draft(self, draft_id: str, **kwargs) -> Dict[str, Any]:
        """
        Get draft by id.
        """
        substack_domain = kwargs.get("substack_domain")
        url = self.build_url(self.base_url(substack_domain), ["publication", "drafts", draft_id])
        response = self._http_client.request("GET", url, authenticated=True)
        return response

    @login_required
    def delete_draft(self, draft_id: str, **kwargs):
        """

        Args:
            draft_id:

        Returns:

        """
        substack_domain = kwargs.get("substack_domain")
        url = self.build_url(self.base_url(substack_domain), ["publication", "drafts", draft_id])
        response = self._http_client.request("DELETE", url, authenticated=True)
        return response

    @login_required
    def update_draft_status(self, draft, **kwargs) -> dict:
        """

        Args:
            draft:
            **kwargs:

        Returns:

        """
        payload = {
            "section_chosen": "false",
            "should_send_email": "true",
            "hide_from_feed": "false",
            "last_updated_at": datetime.now().isoformat(),
            "audience": "everyone",
            # "draft_subtitle": "",
            # "draft_title": "",
        }
        url = self.build_url(self.base_url(), ["publication", "drafts", draft])
        response = self._http_client.request("PUT", url, authenticated=True, data=payload)
        return response

    @login_required
    def create_new_tag(self, tag: str, **kwargs) -> dict:
        """
        Create new tag.

        Args:
            tag: tag name
            **kwargs:

        Returns:

        """
        url = self.build_url(self.base_url(), ["publication", "post-tags"])
        payload = {"name": tag}
        response = self._http_client.request("POST", url, authenticated=True, data=payload)
        return response

    @login_required
    def get_post_tags(self, **kwargs) -> dict:
        """
        Get tags for post.

        Args:
            post_id: post id
            **kwargs:
        """

        url = self.build_url(self.base_url(), ["publication", "post-tag"])
        response = self._http_client.request("GET", url, authenticated=True)
        return response

    @login_required
    def add_tag_to_post(self, post_id: str, tag_id: str, **kwargs) -> dict:
        """
        Add tag to post.

        Args:
            post_id: post id
            tag_id: tag id
            **kwargs:

        Returns:
        "https://strivewithaayush.substack.com/api/v1/post/147486312/tag/f780ef57-b5c5-4073-bd70-defd8eeb42bc"

        """
        url = self.build_url(
            self.base_url(),
            ["post", post_id, "tag", tag_id],
        )
        response = self._http_client.request("POST", url, authenticated=True)
        return response
