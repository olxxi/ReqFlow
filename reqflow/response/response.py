import httpx
from json.decoder import JSONDecodeError
from jsonpath_ng import parse
from typing import Any, Callable


class UnifiedResponse:
    """
    A unified response object.
    """
    def __init__(self, http_response: httpx.Response, response_time: float = None, response_type: str = 'REST'):
        self._status_code = http_response.status_code
        self._headers = http_response.headers
        self._response_time = response_time
        self._raw_body = http_response.content
        self._response_type = response_type
        self._content_type = http_response.headers.get('Content-Type', '')
        self._encoding = http_response.encoding

        try:
            self.cookies = http_response.cookies
        except (RuntimeError, AttributeError):
            self.cookies = None

        if 'application/json' in self.content_type:
            self.body = http_response.json()
        elif 'text/' in self.content_type:
            self.body = http_response.text
        else:
            # For binary data
            self.body = http_response.content

    @property
    def encoding(self) -> str:
        """
        Returns the encoding of the response.

        Returns:
            str: The encoding of the response.
        """
        return self._encoding

    @property
    def content_type(self) -> str:
        """
        Returns the content type of the response from the corresponding header.

        Returns:
            str: The content type of the response.
        """
        return self._content_type

    @property
    def status_code(self) -> int:
        """
        Returns the status code of the response.

        Returns:
            int: The status code of the response.
        """
        return self._status_code

    @property
    def headers(self) -> dict:
        """
        Returns the headers of the response.

        Returns:
            dict: The headers of the response.
        """
        return self._headers

    @property
    def response_type(self) -> str:
        return self._response_type

    @property
    def response_time(self) -> float:
        """
        Returns the response time of the response.

        Returns:
            float: The response time of the response.
        """
        return self._response_time

    @property
    def content(self) -> Any:
        """
        Returns the content of the response.

        Returns:
            Any: The content of the response.
        """
        if self.response_type == 'GRAPHQL' and isinstance(self.body, dict):
            return self.body.get('data', self.body)  # Return 'data' field if it exists
        return self.body  # For REST or non-JSON GraphQL responses

    @property
    def json(self) -> Any:
        return self.body  # Already parsed as JSON or None if invalid

    @property
    def text(self) -> str:
        """
        Returns the text of the response.

        Returns:
            str: The text of the response.
        """
        if self.body is not None:
            return str(self.body)
        return self._raw_body.decode('utf-8')

    @property
    def errors(self):
        """
        Returns the errors of the response.

        Returns:
            Any: The errors of the response.
        """
        if isinstance(self.body, dict):
            return self.body.get('errors')
        return None

    def _assert_json(self, json_path: str, assertion_func: Callable[[Any], None]) -> "UnifiedResponse":
        if self.body is None:
            raise ValueError("Response body is not valid JSON")

        jsonpath_expr = parse(json_path)
        matches = [match.value for match in jsonpath_expr.find(self.body)]
        if not matches:
            raise ValueError(f"JSONPath {json_path} does not match any elements in the JSON response")

        actual_value = matches[0]
        assertion_func(actual_value)  # Use the assertion function

        return self

    def _assert_header(self, header_name: str, assertion_func: Callable[[Any], None]) -> "UnifiedResponse":
        actual_value = self.headers.get(header_name)
        assertion_func(actual_value)
        return self

    def _assert_cookie(self, cookie_name: str, assertion_func: Callable[[Any], None]) -> "UnifiedResponse":
        actual_value = self.cookies.get(cookie_name)
        assertion_func(actual_value)
        return self
