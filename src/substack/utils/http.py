from typing import Any, Dict, Optional

from loguru import logger
from requests import Session

from ..auth import SubstackAuth

HEADERS = {
    "authority": "substack.com",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "dnt": "1",
    "origin": "https://substack.com",
    "priority": "u=1, i",
    "sec-ch-ua": '"Not;A=Brand";v="24", "Chromium";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
}


class HTTPClient:
    def __init__(self, substack_domain: str, auth: SubstackAuth):
        self._substack_domain = substack_domain
        self._auth = auth
        self._session = Session()
        self._cookies = {}

    def request(
        self,
        method: str,
        url: str,
        authenticated: bool = False,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        raw_response: bool = False,
    ) -> Dict[str, Any]:
        headers = HEADERS.copy()
        logger.info(
            f"Making {method} request to {url.upper()} with params: {params} and authentication: {authenticated}"
        )
        if authenticated:
            headers.update(self._auth.get_auth_header())

        response = self._session.request(method.upper(), url, headers=headers, params=params, json=data)
        logger.info(f"Response: {response.status_code} | {response} | {response.text}")
        response.raise_for_status()
        if raw_response:
            return response
        return response.json()

    def get_user_info(self) -> Dict[str, Any]:
        return self._auth.get_user_details()

    @property
    def is_authenticated(self) -> bool:
        return self._auth.is_authenticated
