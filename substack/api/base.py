from abc import ABC
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode, urljoin

from ..utils.http import HTTPClient


class BaseAPI(ABC):
    def __init__(self, http_client: HTTPClient = None):
        self._http_client = http_client

    def base_url(self, substack_subdomain: str = None) -> str:
        if not substack_subdomain:
            return f"https://substack.com/api/v1"
        return f"https://{substack_subdomain}.substack.com/api/v1"

    @staticmethod
    def build_url(
        base_url: str,
        path: Union[str, List[str]],
        query_params: Optional[Dict[str, Any]] = None,
    ) -> str:
        if isinstance(path, list):
            path_str = "/".join(segment.strip("/") for segment in path)
        else:
            path_str = path.lstrip("/")

        url = urljoin(base_url, path_str)

        if query_params:
            return f"{url}?{urlencode(query_params)}"
        return url
