from typing import Any, Dict, Optional

from .client import Client
from reqflow.response.response import UnifiedResponse
from reqflow.validator.validator import Validator
from pydantic import BaseModel
from pydantic import ValidationError
import base64


def given(client: Client):
    """
    Initializes the Given stage with a client (httpx client).

    Args:
        client (Client): The client instance to use for making the request.

    Returns:
        Given: An instance of the Given class initialized with the provided client.
    """
    return Given(client)


class Given:
    """
    Represents the Given stage of the request where you can specify parameters, headers, and the body of the request.
    """

    def __init__(self, client: Client):
        """
        Initializes the Given class with a client.

        Args:
            client (Client): The client instance to use for making the request.
        """
        self.client = client
        self.params = {}
        self.headers = {}
        self.json = None

    def query_param(self, key: str, value: Any):
        """
        Adds a query parameter to the request.

        Args:
            key (str): The key of the query parameter.
            value (Any): The value of the query parameter.

        Returns:
            Given: The instance of the Given class.
        """
        self.params[key] = value
        return self

    def header(self, key: str, value: Any):
        """
        Adds a header to the request.

        Args:
            key (str): The key of the header.
            value (Any): The value of the header.

        Returns:
            Given: The instance of the Given class.
        """
        self.headers[key] = value
        return self

    def headers(self, headers: Dict[str, Any]):
        """
        Adds multiple headers to the request.

        Args:
            headers (Dict[str, Any]): A dictionary of headers to add.

        Returns:
            Given: The instance of the Given class.
        """
        self.headers = headers
        return self

    def body(self, json: Any):
        """
        Sets the JSON body of the request.

        Args:
            json (Any): The JSON body to set for the request.

        Returns:
            Given: The instance of the Given class.
        """
        self.json = json
        return self

    def when(self, method: str, url: str):
        """
        Transitions from the Given stage to the When stage, where the request is made.

        Args:
            method (str): The HTTP method to use.
            url (str): The URL to send the request to.

        Returns:
            When: The instance of the When class.
        """
        return When(self.client, method, url, params=self.params, headers=self.headers, json=self.json)


class When:
    """
    Represents the When stage of the request where the actual request is made.
    """

    def __init__(self, client: Client, method: str, url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, Any]] = None, json: Optional[Any] = None):
        """
        Initializes the When class with the details of the request to be made.

        Args:
            client (Client): The client instance to use for making the request.
            method (str): The HTTP method to use for the request.
            url (str): The URL to send the request to.
            params (Optional[Dict[str, Any]]): Optional dictionary of query parameters.
            headers (Optional[Dict[str, Any]]): Optional dictionary of request headers.
            json (Optional[Any]): Optional JSON body for the request.
        """
        self.client = client
        self.method = method
        self.url = url
        self.params = params or {}
        self.headers = headers or {}
        self.json = json

    def with_auth(self, username: str, password: str):
        """
        Adds basic authentication to the request.

        Args:
            username (str): The username for basic auth.
            password (str): The password for basic auth.

        Returns:
            When: The instance of the When class.
        """
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        self.headers["Authorization"] = f"Basic {encoded_credentials}"
        return self

    def with_oauth2(self, token: str):
        """
        Adds OAuth2 authentication to the request.

        Args:
            token (str): The OAuth2 token to use for auth.

        Returns:
            When: The instance of the When class.
        """
        self.headers["Authorization"] = f"Bearer {token}"
        return self

    def with_api_key(self, key: str, value: str):
        """
        Adds API key authentication to the request.

        Args:
            key (str): The key of the API key.
            value (str): The value of the API key.

        Returns:
            When: The instance of the When class.
        """
        self.headers[key] = value
        return self

    def then(self):
        """
        Transitions from the When stage to the Then stage, where the response is handled.

        Returns:
            Then: The instance of the Then class with the response from the request.
        """
        response = self.client.send(self.method, self.url, params=self.params, headers=self.headers, json=self.json)
        return Then(response, self.client)


class Then:
    """
    Represents the Then stage of the request where the response is handled and assertions are made.
    """

    def __init__(self, response: UnifiedResponse, client: Client):
        """
        Initializes the Then class with the response to handle.

        Args:
            response (UnifiedResponse): The response from the request.
            client (Client): The client instance used for making the request.
        """
        self.response = response
        self.client = client

    def get_response(self):
        """
        Retrieves the response object.

        Returns:
            UnifiedResponse: The response from the request.
        """
        return self.response

    def validate_data(self, expected_model: BaseModel):
        """
        Validates the response data against the expected Pydantic model.

        Args:
            expected_model (BaseModel): The Pydantic model to validate the response data against.

        Raises:
            AssertionError: If the response data does not match the expected model.

        Returns:
            Then: The instance of the Then class.
        """
        validator = Validator(model=expected_model)
        try:
            validator.validate(self.response.content)
        except ValidationError as e:
            raise AssertionError(f"The response data does not match the expected model: {str(e)}")
        return self

    def status_code(self, expected_status_code: int):
        """
        Asserts that the response status code matches the expected status code.

        Args:
            expected_status_code (int): The expected status code of the response.

        Raises:
            AssertionError: If the response status code does not match the expected status code.

        Returns:
            Then: The instance of the Then class.
        """
        assert self.response.status_code == expected_status_code, \
            f"Status code {self.response.status_code} is not {expected_status_code}"
        return self

    def status_code_is_between(self, min_status_code: int, max_status_code: int):
        """
        Asserts that the response status code is within the specified range.

        Args:
            min_status_code (int): The minimum acceptable status code.
            max_status_code (int): The maximum acceptable status code.

        Raises:
            AssertionError: If the response status code is not within the specified range.

        Returns:
            Then: The instance of the Then class.
        """
        assert min_status_code <= self.response.status_code <= max_status_code, \
            f"Status code {self.response.status_code} is not between {min_status_code} and {max_status_code}"
        return self

    def body(self, json_path: str, expected_value: Any):
        """
        Asserts that a specific part of the response body matches the expected value.

        Args:
            json_path (str): The JSONPath expression to locate the part of the response body to assert.
            expected_value (Any): The expected value to compare against.

        Raises:
            ValueError: If the JSONPath does not match any elements in the JSON response.

        Returns:
            Then: The instance of the Then class.
        """
        self.response.assert_json(json_path, expected_value)
        return self

    def get_body(self):
        """
        Retrieves the content of the response body.

        Returns:
            Any: The content of the response body.
        """
        return self.response.content

    def get_header(self, header_name: str):
        """
        Retrieves the value of a specific header from the response.

        Args:
            header_name (str): The name of the header to retrieve.

        Returns:
            str: The value of the specified header.
        """
        return self.response.headers[header_name]

    def get_headers(self):
        """
        Retrieves all headers from the response.

        Returns:
            Dict[str, Any]: A dictionary of all headers in the response.
        """
        return self.response.headers

    def assert_header(self, header_name: str, expected_value: Any):
        """
        Asserts that a specific header matches the expected value.

        Args:
            header_name (str): The name of the header to assert.
            expected_value (Any): The expected value of the header.

        Returns:
            Then: The instance of the Then class.
        """
        self.response.assert_header(header_name, expected_value)
        return self

    def assert_headers(self, headers: Dict[str, Any], excluded_headers: Optional[Dict[str, Any]] = None):
        """
        Asserts that multiple headers in the response match their expected values, except for those explicitly excluded.

        Args:
            headers (Dict[str, Any]): A dictionary where the key is the header name and the value is the expected
            header value.
            excluded_headers (Optional[Dict[str, Any]]): A dictionary of headers to exclude from the assertion.
            The key is the header name.

        Returns:
            Then: The instance of the Then class for fluent chaining.

        Raises:
            AssertionError: If any of the non-excluded headers do not match their expected values.
        """
        for header_name, expected_value in headers.items():
            if excluded_headers and header_name in excluded_headers:
                continue
            self.response.assert_header(header_name, expected_value)
        return self

    def assert_response_time(self, max_time: float):
        """
        Asserts that the response time is less than or equal to the specified maximum time.

        Args:
            max_time (float): The maximum expected response time in seconds.

        Returns:
            Then: The instance of the Then class for fluent chaining.

        Raises:
            AssertionError: If the response time exceeds the maximum expected time.
        """
        assert self.response.response_time <= max_time, \
            f"Response time {self.response.response_time} exceeds the maximum expected time {max_time}"
        return self

    def get_cookies(self):
        """
        Retrieves cookies from the response.

        This method accesses the underlying HTTP client's cookie jar and extracts the cookies as a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representing the cookies received in the response, where the key is
            the cookie name.
        """
        cookies_jar = self.client.http_client.cookies.jar
        cookies_dict = cookies_jar.__dict__.get('_cookies')
        return cookies_dict

    def then(self):
        """
        A placeholder method that simply returns the instance of the Then class.

        This method is typically used at the end of a chain of fluent method calls to signal the end of the chain and
        can be extended for additional functionality if needed.

        Returns:
            Then: The instance of the Then class.
        """
        return self
