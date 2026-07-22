from collections.abc import Callable

from requests import Response

from src.main.api.foundation.endpoint import Endpoint


class HttpRequester:
    def __init__(
        self,
        request_spec: dict[str, str],
        endpoint: Endpoint,
        response_spec: Callable[[Response], None],
    ):
        self.request_spec = request_spec
        self.endpoint = endpoint
        self.response_spec = response_spec
