### Start

Once ReqFlow is installed, start with importing the module along:
```python
from reqflow import given, Client
```

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

!!! note
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

To ensure more integrity of your data, you can use various constrains provided by PyDantic.

```python linenums="1"
from pydantic import BaseModel, Field, EmailStr, constr, condecimal

class Geo(BaseModel):
    lat: condecimal(gt=-90, lt=90)
    lng: condecimal(gt=-180, lt=180)

class Address(BaseModel):
    street: constr(min_length=1, max_length=100)
    suite: constr(min_length=1, max_length=100)
    city: constr(min_length=1, max_length=100)
    zipcode: constr(min_length=5, max_length=10)
    geo: Geo

class Company(BaseModel):
    name: constr(min_length=1, max_length=100)
    catchPhrase: constr(min_length=1, max_length=255)
    bs: constr(min_length=1, max_length=255)

class User(BaseModel):
    id: int
    name: constr(min_length=1, max_length=100)
    username: constr(min_length=1, max_length=100)
    email: EmailStr
    address: Address
    phone: constr(min_length=10, max_length=20, pattern=r'^\+?\d[\d -]{8,12}\d$')
    website: constr(min_length=1, max_length=100)
    company: Company

given(client).when("GET", "/users/1").then()\
    .status_code(200)\
    .validate_data(User)
```

You can also use decimal and float constraints to ensure numeric values fall within specific ranges or meet other conditions.

```python linenums="1"
class FinancialData(BaseModel):
    amount: condecimal(gt=0, max_digits=10, decimal_places=2)
    interest_rate: Field(ge=0.0, le=1.0)

class UserFinancials(BaseModel):
    id: int
    name: str
    balance: FinancialData

given(client).when("GET", "/users/1/financials").then()\
    .status_code(200)\
    .validate_data(UserFinancials)
```

### Upload files

To upload a file to a particular endpoint, use the `file_upload` method specifying the `field_name` and the path to the file:

```python linenums="1"
given(client).file_upload(field_name="userfile", file_path="data/test.png")\
    .when("POST", "/doc/file_upload.html")\
    .then().status_code(200)
```

!!! note
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
# OR
given(url="https://httpbin.org", logging=True).when("GET", "/get?foo=bar").then().status_code(200)

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

### Asynchronous Functionality in ReqFlow

#### Why Use Async in API Testing

Asynchronous programming enhances the performance and responsiveness of applications that involve I/O-bound operations, such as API testing or general network communication. Here are some key benefits:

1. **Concurrent Requests**: Async allows multiple requests to be performed concurrently, which is beneficial when testing endpoints that can handle simultaneous connections.
2. **Improved Performance**: Asynchronous code can lead to better performance and resource utilization since it does not block execution while waiting for I/O operations to complete.
3. **Scalability**: Async is more scalable for applications that need to handle many simultaneous requests, reducing overhead compared to synchronous execution.

#### How to Use Async with ReqFlow

ReqFlow simplifies switching between synchronous and asynchronous requests. To use async functionality, replace the `then` method with `then_async`. Because of the nature of async programming, the `then_async` method returns a coroutine object that needs to be awaited.
Hence, the following validations e.g. `status_code`, `assert_body`, etc. should be performed after awaiting the `then_async` method.

#### Managing the Client

When using async with ReqFlow, it is important to manage the lifecycle of the `Client` to ensure resources are properly cleaned up. There are three primary methods for managing the client:

1. **Direct Instantiation**: Create and close the client within each test.
2. **Context Manager**: Use the `with` context manager to automatically handle client closure.
3. **Use embedded client**: Use the `url` parameter in the `given` method to manage the client lifecycle internally so that the client is created and closed automatically for each request.

##### Using Async with PyTest

To run asynchronous tests with PyTest, use the `pytest-asyncio` plugin, which allows defining async tests with `async def` and using the `pytest.mark.asyncio` decorator.

##### Direct Instantiation

```python linenums="1"
@pytest.mark.asyncio
async def test_get_request_async():
    client = Client(base_url="https://httpbin.org")
    result = await given(client).when("GET", "/get?foo=bar").then_async()
    result.status_code(200).assert_body("args.foo", equal_to("bar"))

@pytest.mark.asyncio
async def test_post_request_async():
    client = Client(base_url="https://httpbin.org")
    payload = {"foo": "bar"}
    result = await given(client).body(payload).when("POST", "/post").then_async()
    result.status_code(200).assert_body("json.foo", equal_to("bar"))
```

##### Context Manager

```python linenums="1"
@pytest.mark.asyncio
async def test_get_request_with_context_manager_async():
    async with Client(base_url="https://httpbin.org") as client:
        result = await given(client).when("GET", "/get?foo=bar").then_async()
        result.status_code(200).assert_body("args.foo", equal_to("bar"))

@pytest.mark.asyncio
async def test_post_request_with_context_manager_async():
    async with Client(base_url="https://httpbin.org") as client:
        payload = {"foo": "bar"}
        result = await given(client).body(payload).when("POST", "/post").then_async()
        result.status_code(200).assert_body("json.foo", equal_to("bar"))
```

##### Using Embedded Client

```python linenums="1"
@pytest.mark.asyncio
async def test_get_request_with_embedded_client_async():
    result = await given(url="https://httpbin.org").when("GET", "/get?foo=bar").then_async()
    result.status_code(200).assert_body("args.foo", equal_to("bar"))

@pytest.mark.asyncio
async def test_post_request_with_embedded_client_async():
    payload = {"foo": "bar"}
    result = await given(url="https://httpbin.org").body(payload).when("POST", "/post").then_async()
    result.status_code(200).assert_body("json.foo", equal_to("bar"))
```

#### Making Concurrent Requests with Async

One of the key advantages of using async is the ability to perform concurrent requests, significantly improving performance when dealing with multiple endpoints or repeated requests.

```python linenums="1"
import pytest
import asyncio
from reqflow import Client, given
from reqflow.assertions import equal_to


@pytest.mark.asyncio
async def test_concurrent_requests():
    async with Client(base_url="https://httpbin.org") as client:
        tasks = [
            given(client).when("GET", "/get?foo=bar").then_async(),
            given(client).when("GET", "/ip").then_async(),
            given(client).when("GET", "/user-agent").then_async()
        ]

        results = await asyncio.gather(*tasks)

        for result in results:
            result.status_code(200)

            
@pytest.mark.asyncio
async def test_concurrent_post_requests():
    async with Client(base_url="https://httpbin.org") as client:
        payloads = [{"foo": f"value{i}"} for i in range(3)]
        tasks = [given(client).body(payload).when("POST", "/post").then_async() for payload in payloads]

        results = await asyncio.gather(*tasks)

        for result in results:
            result.status_code(200).assert_body("json.foo", equal_to(result.request.json["foo"]))
```

#### Performance Comparison - Sync vs Async

To demonstrate the performance benefits of async requests, we can compare the execution time of synchronous and asynchronous tests.

```python linenums="1"
import pytest
import time
import asyncio
from reqflow import Client, given

@pytest.mark.parametrize("test_data", [
    (["/get", "/ip", "/user-agent"], [{"test": f"value{i}"} for i in range(50)])
])
def test_sync_performance(test_data):
    endpoints, param_list = test_data
    client = Client(base_url="https://httpbin.org")

    start_time = time.time()

    results = []
    for params in param_list:
        for endpoint in endpoints:
            result = given(client).query_param(params).when("GET", endpoint).then()
            results.append(result)
            result.status_code(200)

    end_time = time.time()

    total_duration = end_time - start_time
    print(f"Synchronous requests to {endpoints} with diverse params total duration: {total_duration} seconds")


@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", [
    (["/get", "/ip", "/user-agent"], [{"test": f"value{i}"} for i in range(50)])
])
async def test_async_performance(test_data):
    endpoints, param_list = test_data
    async with Client(base_url="https://httpbin.org") as client:
        start_time = time.time()

        tasks = [
            given(client).query_param(params).when("GET", endpoint).then_async()
            for params in param_list
            for endpoint in endpoints
        ]

        results = await asyncio.gather(*tasks)

        end_time = time.time()

        total_duration = end_time - start_time
        print(f"Asynchronous requests to {endpoints} with diverse params total duration: {total_duration} seconds")

        for result in results:
            result.status_code(200)
```

As a result, the asynchronous test will complete significantly faster (**2.7 sec**) than the synchronous test (**39 sec**) due to the concurrent execution of requests:

```bash
======================= 2 passed, in 41.79s =======================
PASSED                        [ 50%]Synchronous requests to ['/get', '/ip', '/user-agent'] with diverse params total duration: 38.94446110725403 seconds
PASSED                       [100%]Asynchronous requests to ['/get', '/ip', '/user-agent'] with diverse params total duration: 2.7714710235595703 seconds
```

