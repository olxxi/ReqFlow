from typing import Any, Dict, Optional, Union, Type

from .client import Client
from reqflow.response.response import UnifiedResponse
from reqflow.validator.validator import Validator
from reqflow.exceptions import GivenInitializationError, InvalidArgumentError, InvalidCredentialsError
from pydantic import BaseModel
from pydantic import ValidationError
import base64

import os

# Client optional, can be run just with the url
def given(client: Optional[Client] = None, url: Optional[str] = None, logging: Optional[bool] = False) -> 'Given':
    """
    Initializes the Given stage with a client instance or a URL. If
    the client is not provided, the URL can be provided directly.

    Args:
        client (Client): The client instance to use for making the request.
        url: If the client is not provided, the URL can be provided directly.
            The client will be initialized with the URL as base_url.
        logging (bool): If True, logs will be stored in GlobalLogger class.

    Examples:
        >>> from reqflow import given, Client
        >>> client = Client(base_url="https://url.com")
        >>> given(client).when("GET", "/path").then().status_code(200)
        >>> # OR
        >>> given(url="https://url.com").when("GET", "/path").then().status_code(200)
        >>> # OR
        >>> given(url="https://url.com", logging=True).when("GET", "/path").then().status_code(200)

    Returns:
        Given (class): An instance of the Given class initialized with the provided client.
    """

    if client:
        if url or logging:
            raise GivenInitializationError("If client is provided, url and logging parameters are not accepted",
                                           {'client': client, 'url': url, 'logging': logging})
        return Given(client)
    elif url:
        return Given(Client(base_url=url, logging=logging))
    else:
        raise GivenInitializationError("Client or URL must be provided",
                                       {'client': client, 'url': url, 'logging': logging})

class Given:
    """
    Represents the Given stage of the request where you can specify parameters, headers, cookies
    and the body of the request.

    Args:
        client (Client): The client instance to use for making the request.

    """

    def __init__(self, client: Client):
        self.client = client
        self.params = {}
        self.request_headers = {}
        self.request_cookies = {}
        self.json = None
        self.data = None
        self.files = {}

    def query_param(self, params: Dict[str, Any]) -> 'Given':
        """
        Adds a query parameter to the request.

        Args:
            params (Dict[str, Any]): A dictionary of query parameters to add.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> params = {'chocolate': 'chip'}
            >>> r = given(client).query_param(params).when("GET", "/cookies/set").then()...

        Returns:
            Given: The instance of the Given class.
        """
        if not isinstance(params, dict):
            raise InvalidArgumentError("The `params` argument must be a dictionary.")

        self.params = params
        return self

    def cookies(self, cookies: Dict[str, Any]) -> 'Given':
        """
        Adds multiple cookies to the request.

        Args:
            cookies (Dict[str, Any]): A dictionary of cookies to add.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> cks = {"cookie1": "value1", "cookie2": "value2"}
            >>> given(client).cookies(cks).when("GET", "/cookies").then()...

        Returns:
            Given: The instance of the Given class.
        """
        if not isinstance(cookies, dict):
            raise InvalidArgumentError("The `cookies` argument must be a dictionary.")

        self.request_cookies = cookies
        return self

    def header(self, key: str, value: str) -> 'Given':
        """
        Adds a header to the request.

        Args:
            key (str): The key of the header.
            value (Any): The value of the header.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> given(client).header("Authorization", "Bearer TOKEN").when("GET", "/headers").then()...

        Returns:
            Given: The instance of the Given class.
        """
        if not isinstance(key, str) or not isinstance(value, str):
            raise InvalidArgumentError("Both `key` and `value` arguments must be strings.")

        self.request_headers[key] = value
        return self

    def headers(self, headers: Dict[str, Any]) -> 'Given':
        """
        Adds multiple headers to the request.

        Args:
            headers (Dict[str, Any]): A dictionary of headers to add.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> HEADERS = {'Authorization': 'Bearer TOKEN', 'test_header': 'test_value'}
            >>> given(client).headers(HEADERS).\
                  when("GET", "/headers").\
                  then()...

        Returns:
            Given: The instance of the Given class.
        """
        if not isinstance(headers, dict):
            raise InvalidArgumentError("The `headers` argument must be a dictionary.")

        self.request_headers = headers
        return self

    def body(self, content: Union[dict, None] = None, *, json: Any = None, data: Any = None) -> 'Given':
        """
        Sets the body of the request. Either `json` or `data` can be set, but not both.

        Args:
            content (dict, optional): Shortcut for setting JSON data directly. Defaults to None.
            json (Any, optional): The JSON body to set for the request. Defaults to None.
            data (Any, optional): The form data to send in the body of the request. Defaults to None.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> # Using `content` as a shortcut for JSON data
            >>> given(client).body({"key": "value"}).when("POST", "/post").then()...
            >>> # Explicitly using `json` parameter
            >>> given(client).body(json={"key": "value"}).when("POST", "/post").then()...
            >>> # Using `data` for form data
            >>> given(client).body(data="key=value").when("POST", "/post").then()...

        Raises:
            ValueError: If both `json` and `data` are provided.

        Returns:
            Given: The instance of the Given class.
        """
        if content:
            if json is not None or data is not None:
                raise ValueError("Cannot set both `content` and `json` or `data`")
            self.json = content
        else:
            if json is not None and data is not None:
                raise ValueError("Cannot set both `json` and `data` for the request")
            self.json = json
            self.data = data

        return self

    def file_upload(self, field_name: str, file_path: str) -> 'Given':
        """
        Sets the file to upload for the request.
        Args:
            field_name (str): The name of the form field the file is associated with.
            file_path (str): The path to the file to be uploaded.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> given(client).file_upload("userfile", "data/test.png").\
            >>>     when("POST", "/doc/file_upload.html").then()...

        Note:
            `field_name` must be the same as the name of the form field in the request.

        Returns:
            Given: The instance of the Given class for chaining.
        """
        try:
            with open(file_path, 'rb') as f:
                self.files[field_name] = (os.path.basename(file_path), f.read())
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_path} not found")
        return self

    def when(self, method: str, url: Optional[str] = "") -> 'When':
        """
        Transitions from the Given stage to the When stage, where the request is made.

        Args:
            method (str): The HTTP method to use.
            url (str): The URL to send the request to.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> given(client).when("GET", "/get").then()...

        Note:
            If the `url` is not provided, the `url` provided in the Client instance will be used.

        Returns:
            When: The instance of the When class.
        """
        return When(self.client, method, url, params=self.params, headers=self.request_headers, json=self.json,
                    data=self.data, cookies=self.request_cookies, files=self.files)


class When:
    """
    Represents the When stage of the request where the actual request is made.
    """

    def __init__(self, client: Client, method: str, url: Optional[str] = "", params: Optional[Dict[str, Any]] = None,
                 headers: Optional[Dict[str, Any]] = None, json: Optional[Any] = None, data: Optional[Any] = None,
                 cookies: Optional[Dict[str, Any]] = None, files: Optional[Dict[str, Any]] = None):
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
        self.cookies = cookies or {}
        self.json = json
        self.data = data
        self.files = files

    def with_auth(self, username: str, password: str) -> 'When':
        """
        Adds basic authentication to the request.

        Args:
            username (str): The username for basic auth.
            password (str): The password for basic auth.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> given(client).when("GET", "/basic-auth/user/pass").with_auth("user", "pass").then()...

        Returns:
            When: The instance of the When class.
        """
        if not isinstance(username, str) or not isinstance(password, str):
            raise InvalidCredentialsError("The `username` and `password` arguments must be strings.")

        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        self.headers["Authorization"] = f"Basic {encoded_credentials}"
        return self

    def with_oauth2(self, token: str) -> 'When':
        """
        Adds OAuth2 authentication to the request.

        Args:
            token (str): The OAuth2 token to use for auth.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> token = "some_token"
            >>> given(client).when("GET", "/bearer").with_oauth2(token).then()...

        Returns:
            When: The instance of the When class.
        """
        if not isinstance(token, str):
            raise InvalidCredentialsError("The `token` argument must be a string.")

        self.headers["Authorization"] = f"Bearer {token}"
        return self

    def with_api_key(self, key: str, value: str) -> 'When':
        """
        Adds API key authentication to the request.

        Args:
            key (str): The key of the API key.
            value (str): The value of the API key.

        Returns:
            When: The instance of the When class.
        """
        if not isinstance(key, str) or not isinstance(value, str):
            raise InvalidCredentialsError("The `key` and `value` arguments must be strings.")

        self.headers[key] = value
        return self

    def then(self, follow_redirects: bool = False, timeout: float = 5.0) -> 'Then':
        """
        Transitions from the When stage to the Then stage, where the response is handled.

        Args:
            timeout: The timeout for the request in seconds. Defaults to 5.0.
            follow_redirects (bool): httpx parameter to follow redirects or not. Defaults to False.

        Note:
            The actual request is made when this method is called.

        Returns:
            Then: The instance of the Then class with the response from the request.
        """
        response = self.client.send(self.method, self.url, params=self.params, headers=self.headers,
                                    json=self.json, data=self.data, cookies=self.cookies, redirect=follow_redirects,
                                    files=self.files, timeout=timeout)
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

    def get_response(self) -> UnifiedResponse:
        """
        Retrieves the response object.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> r = given(client).when("GET", "/get").then().get_response()
            >>> r.status_code
            >>> 200

        Returns:
            UnifiedResponse: The response from the request.
        """
        return self.response

    def validate_data(self, expected_model: Type[BaseModel]) -> 'Then':
        """
        Validates the response data against the expected Pydantic model.

        Args:
            expected_model (Type[BaseModel]): The Pydantic model to validate the response data against.

        Raises:
            AssertionError: If the response data does not match the expected model.

        Examples:
            >>> from reqflow import given, Client
            >>> from pydantic import BaseModel
            >>>
            >>> client = Client(base_url="https://httpbin.org")
            >>>
            >>> class Data(BaseModel):
            >>>     url: str
            >>>     args: dict
            >>>     headers: dict
            >>>     origin: str
            >>>     method: str
            >>>     ...
            >>> given(client).when("GET", "/get").then().validate_data(Data)

        Returns:
            Then: The instance of the Then class.
        """
        validator = Validator(model=expected_model)
        try:
            validator.validate(self.response.content)
        except ValidationError as e:
            raise AssertionError(f"The response data does not match the expected model: {str(e)}")
        return self

    def status_code(self, expected_status_code: int) -> 'Then':
        """
        Asserts that the response status code matches the expected status code.

        Args:
            expected_status_code (int): The expected status code of the response.

        Raises:
            AssertionError: If the response status code does not match the expected status code.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> given(client).when("GET", "/get").then().status_code(200)

        Returns:
            Then: The instance of the Then class.
        """
        assert self.response.status_code == expected_status_code, \
            f"Status code {self.response.status_code} is not {expected_status_code}"
        return self

    def status_code_is_between(self, min_status_code: int, max_status_code: int) -> 'Then':
        """
        Asserts that the response status code is within the specified range.

        Args:
            min_status_code (int): The minimum acceptable status code.
            max_status_code (int): The maximum acceptable status code.

        Raises:
            AssertionError: If the response status code is not within the specified range.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> given(client).when("GET", "/get").then().status_code_is_between(200, 299)

        Returns:
            Then: The instance of the Then class.
        """
        assert min_status_code <= self.response.status_code <= max_status_code, \
            f"Status code {self.response.status_code} is not between {min_status_code} and {max_status_code}"
        return self

    def assert_body(self, json_path: str, expected_value: Any) -> 'Then':
        """
        Asserts that a specific part of the response body matches the expected value.

        Args:
            json_path (str): The JSONPath expression to locate the part of the response body to assert.
            expected_value (Any): The expected value to compare against.

        Raises:
            ValueError: If the JSONPath does not match any elements in the JSON response.

        Examples:
            >>> from reqflow import given, Client
            >>> from reqflow.assertions import equal_to
            >>>
            >>> client = Client(base_url="https://httpbin.org")
            >>>
            >>> payload = {"foo": "bar"}
            >>> given(client).body(payload).when("POST", "/post").then().assert_body("json.foo", equal_to("bar"))

        Note:
            The `jsonpath-ng` expression is evaluated against the response body as a JSON object.

        Returns:
            Then: The instance of the Then class.
        """
        self.response._assert_json(json_path, expected_value)
        return self

    def get_content(self) -> Any:
        """
        Retrieves the content of the response body.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> r = given(client).when("GET", "/get").then().get_content()

        Returns:
            Any: The content of the response body.
        """
        return self.response.content

    def get_header(self, header_name: str) -> Any:
        """
        Retrieves the value of a specific header from the response.

        Args:
            header_name (str): The name of the header to retrieve.

        Examples
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> r = given(client).when("GET", "/get").then().get_header("Content-Type")
            >>> r
            >>> "application/json"

        Returns:
            str: The value of the specified header.
        """
        try:
            header = self.response.headers[header_name]
        except KeyError:
            raise KeyError(f"Header {header_name} not found in response")
        return header

    def get_headers(self) -> Dict[str, Any]:
        """
        Retrieves all headers from the response.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> r = given(client).when("GET", "/get").then().get_headers()
            >>> r
            >>> {"Content-Type": "application/json", "Content-Length": "123"}

        Returns:
            Dict[str, Any]: A dictionary of all headers in the response.
        """
        return self.response.headers

    def get_encoding(self) -> str:
        """
        Retrieves the encoding of the response.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> r = given(client).when("GET", "/get").then().get_encoding()
            >>> r
            >>> "utf-8"

        Returns:
            str: The encoding of the response.
        """
        return self.response.encoding

    def assert_header(self, header_name: str, expected_value: Any) -> 'Then':
        """
        Asserts that a specific header matches the expected value.

        Args:
            header_name (str): The name of the header to assert.
            expected_value (Any): The expected value of the header.

        Examples:
            >>> from reqflow import given, Client
            >>> from reqflow.assertions import equal_to
            >>> client = Client(base_url="https://httpbin.org")
            >>> given(client).when("GET", "/get").then().assert_header("Content-Type", equal_to("application/json"))

        Returns:
            Then: The instance of the Then class.
        """
        self.response._assert_header(header_name, expected_value)
        return self

    def assert_header_exists(self, header_name: str) -> 'Then':
        """
        Asserts that a specific header exists in the response.

        Args:
            header_name (str): The name of the header to assert.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> given(client).when("GET", "/get").then().assert_header_exists("Content-Type")

        Returns:
            Then: The instance of the Then class.
        """
        assert header_name in self.response.headers, f"Header {header_name} does not exist in the response"
        return self

    def assert_response_time(self, max_time: float) -> 'Then':
        """
        Asserts that the response time is less than or equal to the specified maximum time.

        Args:
            max_time (float): The maximum expected response time in seconds.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> given(client).when("GET", "/get").then().assert_response_time(1.0)

        Returns:
            Then: The instance of the Then class for fluent chaining.

        Raises:
            AssertionError: If the response time exceeds the maximum expected time.
        """
        assert self.response.response_time <= max_time, \
            f"Response time {self.response.response_time} exceeds the maximum expected time {max_time}"
        return self

    def assert_cookie(self, cookie_name: str, expected_value: Any) -> 'Then':
        """
        Asserts that a specific cookie matches the expected value.

        Args:
            cookie_name (str): The name of the cookie to assert.
            expected_value (Any): The expected value of the cookie.

        Examples:
            >>> from reqflow import given, Client
            >>> from reqflow.assertions import equal_to
            >>> client = Client(base_url="https://httpbin.org")
            >>> given(client).query_param('chocolate', 'chip').when("GET", "/cookies/set").then()\
            >>>                                      .assert_cookie("chocolate", equal_to("chip"))

        Returns:
            Then: The instance of the Then class.
        """
        self.response._assert_cookie(cookie_name, expected_value)
        return self

    def get_cookies(self) -> Dict[str, Any]:
        """
        Retrieves all cookies from the response.

        Examples:
            >>> client = Client(base_url="https://httpbin.org")
            >>> given(client).query_param('chocolate', 'chip').when("GET", "/cookies/set").then().get_cookies()
            >>> {'chocolate': 'chip'}
        Returns:
            dict: A dictionary of all cookies in the response.
        """
        return dict(self.response.cookies)

    def save_response_to_file(self, file_path: str) -> 'Then':
        """
        Saves the response content to a specified file. Useful for downloading files.

        Args:
            file_path (str): The path where the response content should be saved.

        Examples:
            >>> from reqflow import given, Client
            >>> client = Client(base_url="https://httpbin.org")
            >>> given(client).when("GET", "/image/png").then().save_response_to_file("image.png")

        Returns:
            Then: The instance of the Then class.
        """
        content_type = self.response.headers.get('Content-Type', '')

        try:
            if 'text' in content_type or 'application/json' in content_type:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.response.json)
            else:
                with open(file_path, 'wb') as file:
                    file.write(
                        self.response.body if isinstance(self.response.body, bytes)
                        else self.response.json.encode('utf-8'))
        except IOError as e:
            raise Exception(f"Error saving file: {e}")

        return self
