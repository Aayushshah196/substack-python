from abc import ABC
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode, urljoin

from loguru import logger

from ..utils.http import HTTPClient


class BaseAPI(ABC):
    def __init__(self, http_client: HTTPClient = None, substack_subdomain: str = None):
        self._site_base_url = "https://substack.com/api/v1"
        self._http_client = http_client
        self._substack_subdomain = substack_subdomain

    def base_url(self, substack_subdomain: str = None) -> str:
        if substack_subdomain:
            return f"https://{substack_subdomain}.substack.com/api/v1"
        elif self._substack_subdomain:
            return f"https://{self._substack_subdomain}.substack.com/api/v1"
        raise ValueError("Substack subdomain not provided")

    @staticmethod
    def build_url(
        base_url: str,
        path: Union[str, List[str]],
    ) -> str:
        if isinstance(path, list):
            path_str = "/".join(str(segment).strip("/") for segment in path)
        else:
            path_str = path.lstrip("/")
        if not base_url.endswith("/"):
            base_url += "/"
        url = urljoin(base_url, path_str)
        return url

    def get_categories(
        self,
    ) -> Dict[str, Any]:
        url = self.build_url(self._site_base_url, ["categories"])
        return self._http_client.request("GET", url, authenticated=False)
