import httpx
from json.decoder import JSONDecodeError
from jsonpath_ng import parse
from typing import Any, Callable


class UnifiedResponse:
    def __init__(self, http_response: httpx.Response, response_time: float = None, response_type: str = 'REST'):
        self.status_code = http_response.status_code
        self.headers = http_response.headers
        self.response_time = response_time
        self._raw_body = http_response.content
        self.response_type = response_type
        try:
            self.body = http_response.json()
        except JSONDecodeError:
            self.body = None  # Set to None if it's not a valid JSON

    @property
    def content(self):
        if self.response_type == 'GRAPHQL' and isinstance(self.body, dict):
            return self.body.get('data', self.body)  # Return 'data' field if it exists
        return self.body  # For REST or non-JSON GraphQL responses

    @property
    def json(self) -> Any:
        return self.body  # Already parsed as JSON or None if invalid

    @property
    def text(self) -> str:
        if self.body is not None:
            return str(self.body)
        return self._raw_body.decode('utf-8')

    # @property
    # def data(self):
    #     if isinstance(self.body, dict):
    #         return self.body.get('data')
    #     return None

    @property
    def errors(self):
        if isinstance(self.body, dict):
            return self.body.get('errors')
        return None

    def assert_json(self, json_path: str, assertion_func: Callable[[Any], None]) -> "UnifiedResponse":
        if self.body is None:
            raise ValueError("Response body is not valid JSON")

        jsonpath_expr = parse(json_path)
        matches = [match.value for match in jsonpath_expr.find(self.body)]
        if not matches:
            raise ValueError(f"JSONPath {json_path} does not match any elements in the JSON response")

        actual_value = matches[0]
        assertion_func(actual_value)  # Use the assertion function

        return self

    def assert_header(self, header_name: str, assertion_func: Callable[[Any], None]) -> "UnifiedResponse":
        actual_value = self.headers.get(header_name)
        assertion_func(actual_value)
        return self


