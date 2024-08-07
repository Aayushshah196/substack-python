from typing import Any, Dict, Optional

from requests import Session

from ..auth import SubstackAuth


class HTTPClient:
    def __init__(self, substack_domain: str, auth: SubstackAuth):
        self._substack_domain = substack_domain
        self._auth = auth
        self._session = Session()

    def request(
        self,
        method: str,
        url: str,
        authenticated: bool = False,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        headers = {}
        if authenticated:
            headers.update(self._auth.get_auth_header())

        response = self._session.request(method, url, headers=headers, params=params, json=data)
        response.raise_for_status()
        return response.json()
