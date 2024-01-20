from typing import Any, Dict, Optional


class Request:
    def __init__(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        json: Optional[Any] = None,
    ):
        self.method = method
        self.url = url
        self.params = params or {}
        self.headers = headers or {}
        self.json = json

    def with_params(self, **params) -> "Request":
        self.params.update(params)
        return self

    def with_headers(self, **headers) -> "Request":
        self.headers.update(headers)
        return self

    def with_json(self, json: Any) -> "Request":
        self.json = json
        return self
