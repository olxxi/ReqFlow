# ReqFlow

![PyPI - Version](https://img.shields.io/pypi/v/reqflow)
![Python - version](https://img.shields.io/badge/python-3.8+-blue.svg)
[![Downloads](https://static.pepy.tech/badge/reqflow)](https://pepy.tech/project/reqflow)

ReqFlow is a Python library designed for efficient and intuitive API testing. 
ReqFlow offers a fluent and flexible interface for crafting and validating HTTP requests, 
making API testing both straightforward and adaptable. While it make sense to use standard approaches for a Python API
testing, ReqFlow reduces the entry barrier for beginners and allows for more advanced use cases with RestAssured-like
approach. 

### Features

* Fluent API for building and sending HTTP requests.
* Supports response handling and validations.
* Customizable response validation using `PyDantic` models.
* Convenient utility methods for common assertions and response manipulations.

The tool is still in development, braking changes are possible. Any feedback and contributions are highly appreciated.

### Documentation
Detailed documentation can be found at [reqflow.org](https://reqflow.org/)

### Installation

Install ReqFlow using `pip`:

```shell
pip install reqflow 
```


### Quick Start

#### Contents

* [Send a Request](#quick-start)
* [Headers](#headers)
* [Query parameters](#query-parameters)
* [Response](#response-operations)
* [Cookies](#cookies)
* [Authentication](#authentication)
* [Assertions](#assertions)
* [PyDantic Response Validation](#pydantic-response-validation)
* [Upload files](#upload-files)
* [Download files](#download-files)
* [Logging and PyTest Integration](#logging)

Let's make a simple request to [HTTPBin](https://httpbin.org) API by create a new client and making a 
`GET` request to the `/get` endpoint and asserting the response status code is `200`:

```python linenums="1"
client = Client("https://httpbin.org")
given(client).when("GET", "/get").then().status_code(200)
```

Alternatively, the request can be sent without explicitly defined client object:

```python linenums="1"
given(url="https://httpbin.org").when("GET", "/get").then().status_code(200)
```
For other HTTP methods, you can use the `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS` parameters:

```python linenums="1"
PAYLOAD = {"foo": "bar"}

given(client).body(PAYLOAD).when("POST", "/post").then()...

given(client).body(PAYLOAD).when("PUT", "/put").then()...

given(client).body(PAYLOAD).when("PATCH", "/patch").then()...

given(client).when("DELETE", "/delete").then()...

...
```

### Headers
To set a header for your request, one can use the `header` method traling the `given` method:

```python linenums="1"
given(client).header("Content-Type", "application/json")\
    .when("POST", "/post")\
    .then()...
```

In case you want to set multiple headers, you can use the `headers` method:

```python linenums="1"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

given(client).headers(HEADERS).when("POST", "/post").then()...
```

To retrieve one or multiple response headers:

```python linenums="1"

hdr = given(client).when("GET", "/get").then().get_header("Content-Type")
hdr
>>> "application/json"

hdrs = given(client).when("GET", "/get").then().get_headers()
hdrs
>>> {"Content-Type": "application/json", "Content-Length": "1234", ...}
```

### Query parameters
To set up query parameters in the URL, use the `query_param` method:

```python linenums="1"
PARAMS = {"foo": "bar"}
given(client).query_param(PARAMS).when("GET", "/get").then()...
```

### Response operations
If you want to retrieve the response object, you can use the `then.().get_response()` method:

```python linenums="1"
r = given(client).when("GET").then().get_response()
r
>>> <UnifiedResponse object at 0x108f81es0>
```

The API reference for the `UnifiedResponse` object can be found [here](https://olxxi.github.io/ReqFlow/response/).

To retrieve the response content, you can use the `then.().get_content()` method:

```python linenums="1"
data = given(client).when("GET").then().get_content()
data
>>> {...}
```

### Cookies

To set a cookie for your request, one can use the `cookie` method trailing the `given` method:

```python linenums="1"
cks = {"cookie1": "value1", "cookie2": "value2"}
given(client).cookies(cks).when("GET", "https://httpbin.org/cookies")\
    .then()...
```

To retrieve one or multiple response cookies:

```python linenums="1"
cks = given(client).when("GET", "https://httpbin.org/cookies")\
    .then().get_cookies()
ck
>>> {"cookie1": "value1", "cookie2": "value2"}
```

### Authentication
Reqflow supports the following authentication methods:
* Basic Authentication
* OAuth2.0 Authentication
* API Keys

#### Basic Authentication
To set up basic authentication, use the `with_auth` method trailing the `when` method:

```python linenums="1"
given(client)\
        .when("GET", "/basic-auth/user/passwd").with_auth("user", "passwd")\
        .then()...
```

#### OAuth2 Authentication (Bearer Token)
The Bearer token can be set either explicitly in header or via the `with_oauth2` method:

```python linenums="1"
given(client).when("GET", "/bearer").with_oauth2(token)\
        .then()...
```

#### API Keys
API Key authorization method represents a wrapper for setting a header with a known name and value in the form of an API key.

```python linenums="1"
given(client).when("GET", "/bearer").with_api_key(HEADER_NAME, API_KEY)\
        .then()...
```


### Assertions

ReqFlow provides a set of assertions to validate the response parameters as well as the embedded assertion functions
to validate the response content.

#### Assertion Functions
The following embedded assertion functions are available:

* `contains_string()`
* `equal_to()`
* `not_equal_to()`
* `greater_than()`
* `less_than()`
* `list_contains()`
* `is_none()`
* `is_not_none()`
* `matches_regex()`
* `and_(*assertion_functions)`
* `or_(*assertion_functions)`

The list of assertion functions and with the descriptions can be found [here](https://olxxi.github.io/ReqFlow/assertions/).

#### Status Code

```python linenums="1"
given(client).when("GET", "/get").then().status_code(200)
```

#### Response Time

```python linenums="1"
given(client).when("GET", "/get?foo=bar").then()\
    .assert_response_time(max_time=0.5)
```

#### Cookies
    
```python linenums="1"
given(client).query_param(params).when("GET", "/cookies/set").then()\
        .assert_cookie('chocolate', equal_to('chip'))
```

#### Headers

```python linenums="1"
    given(client).when("GET", "/get?foo=bar")\
        .then().assert_header("Content-Type", equal_to("application/json"))
```

#### Response Content
To validate a specific response content value, the `assert_body` can be used along with the embedded assertion functions.
The parameter search is implemented by using the [`jsonpath-ng`](https://pypi.org/project/jsonpath-ng/) package.

```python linenums="1"
given(client).when("GET", "/get?foo=bar").then()\
    .status_code(200).\
    assert_body("args.foo", equal_to("bar"))
```

### PyDantic Response Validation

PyDantic integration allows to define precise data structures and use them as a blueprint for the response validation.
The validation is performed by the `validate_data` method and passing the PyDantic model as a parameter.

```python linenums="1"
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    username: str
    email: str
    address: dict
    phone: str
    website: str
    company: dict
    
given(client).when("GET", "/users/1").then()\
    .status_code(200)\
    .validate_data(User)
```

### Upload files

To upload a file to a particular endpoint, use the `file_upload` method specifying the `field_name` and the path to the file:

```python linenums="1"
given(client).file_upload(field_name="userfile", file_path="data/test.png")\
    .when("POST", "/doc/file_upload.html")\
    .then().status_code(200)
```

`field_name` must be the same as the name of the form field in the request.

### Download files

To download a file or save the response content to a file with a desired format, use the `save_response_to_file` method specifying the `file_path` parameter:

```python linenums="1"
given(client).when("GET").then()\
    .status_code(200)\
    .save_response_to_file(file_path="file.pdf")
```

### Logging

ReqFlow supports logging to aggregate the test results and provide a detailed overview of the execution across all client objects. 
To enable logging, set the `logging` argument to `True` when creating a new client object:

```python linenums="1"
client = Client("https://httpbin.org", logging=True)
```

With the `logging` enabled, all requests/responses made by the client object will be stored in the `GlobalLogger` object

```python linenums="1"
from reqflow.utils.logger import GlobalLogger
from reqflow import Client, given

client = Client(base_url="https://httpbin.org", logging=True)
given(client).when("GET", "/get?foo=bar").then().status_code(200)

logs = GlobalLogger.get_logs()
print(logs)

>>> [
        {'function': 'test_function_name',
        'request': {...request details...},
        'response': {...response details...}
    ]
```

The logger saves the following information:
* `function` - the name of the test function (or the function from where the `then` method was called)
* `request` - the request details (method, url, headers, body, query parameters, redirect and timeout options, cookies)
* `response` - the response details (status code, headers, content, cookies, response time)

#### Generating Reports
##### HTML Report
To generate an HTML report, use the `generate_html_report` method from the `GlobalLogger` object:

```python linenums="1"
from reqflow.utils.logger import GlobalLogger
from reqflow import Client, given

client = Client(base_url="https://httpbin.org", logging=True)
given(client).when("GET", "/get?foo=bar").then().status_code(200)

GlobalLogger.generate_html_report(file_path="/path/to/report.html", report_title="Smoke Test")
```

##### JSON Report
To generate a JSON report, use the `generate_json_report` method from the `GlobalLogger` object:

```python linenums="1"
from reqflow.utils.logger import GlobalLogger
from reqflow import Client, given

client = Client(base_url="https://httpbin.org", logging=True)
given(client).when("GET", "/get?foo=bar").then().status_code(200)
# OR
given(url="https://httpbin.org", logging=True).when("GET", "/get?foo=bar").then().status_code(200)


GlobalLogger.generate_json_report(file_path="/path/to/report.json")
```

#### PyTest Integration
To integrate ReqFlow reporting/logging with PyTest, one can use PyTest's fixtures and hooks in the `conftest.py` file:

```python linenums="1"
import pytest
from reqflow.utils.logger import GlobalLogger

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    yield

@pytest.hookimpl
def pytest_sessionfinish(session, exitstatus):
    logs = GlobalLogger.get_logs()
    if logs:
        GlobalLogger.generate_html_report(file_path="test_report.html", report_title="Aggregated Requests")
        GlobalLogger.generate_json_report(file_path="test_report.json")
    GlobalLogger.clear_logs()
```

With the example above, the report will be generated after the test session is finished. 
The results will be aggregated across all test functions and clients within the session.



