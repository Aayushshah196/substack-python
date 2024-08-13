from functools import wraps

from loguru import logger

from ..errors import AuthenticationError


def login_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self._http_client._auth, "is_authenticated"):
            raise AttributeError("_auth has no 'is_authenticated' attribute")

        if not self._http_client._auth.is_authenticated:
            raise AuthenticationError("This method requires authentication. Please login first.")
        return func(self, *args, **kwargs)

    return wrapper
