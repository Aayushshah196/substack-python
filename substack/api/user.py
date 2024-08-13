from typing import Any, Dict

from ..utils.decorators import login_required
from .base import BaseAPI


class UserAPI(BaseAPI):

    def get_user(self) -> Dict[str, Any]:
        url = f"{self.base_url}/user"
        return self._http_client.request("GET", url, authenticated=True)

    @login_required
    def get_user_settings(self) -> Dict[str, Any]:
        # GET: "https://strivewithaayush.substack.com/api/v1/user-setting"
        url = self.build_url(self.base_url(), ["setting"])
        response = self._http_client.request("GET", url, authenticated=True)
        return response

    @login_required
    def update_user_settings(self, **kwargs) -> Dict[str, Any]:
        # PUT: "https://strivewithaayush.substack.com/api/v1/user-setting"
        # payload = {type: "prepublish_subscribe_cta_prompt_hidden", value_bool: true}
        url = f"{self.base_url}/user"
        return self._http_client.request("PUT", url, authenticated=True, data=kwargs)

    @login_required
    def get_user_subscriptions(self, **kwargs) -> Dict[str, Any]:
        # https://strivewithaayush.substack.com/api/v1/subscriptions
        url = self.build_url(self.base_url(), ["subscriptions"])
        response = self._http_client.request("GET", url, authenticated=True)
        return response

    def get_user_details(self, user_id: str, username: str) -> Dict[str, Any]:
        # endpoint = 'https://substack.com/api/v1/user/106455990-bytebytego/public_profile/self'
        url = self.build_url(
            self._site_base_url,
            ["user", f"{user_id}-{username}", "public_profile", "self"],
        )
        response = self._http_client.request("GET", url, authenticated=False)
        return response

    def get_self_details(self):
        if not self._http_client._auth.is_authenticated:
            raise ValueError("User not authenticated")
        user_details = self._http_client.get_user_info()
        return self.get_user_details(user_details.get("id"), user_details.get("username"))
