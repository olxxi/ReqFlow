### Start

Once ReqFlow is installed, start with importing the module along::
```python
from reqflow import given, Client
```

Let's make a simple request to [HTTPBin](https://httpbin.org) API by create a new client and making a 
`GET` request to the `/get` endpoint and asserting the response status code is `200`:

```python linenums="1"
client = Client("https://httpbin.org")
given(client).when("GET", "/get").then()status_code(200)
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

### Pass query parameters
### Get response/response content

### Cookies
### Authentication
### Assertions
### PyDantic Validation
### Upload/Download files (save as any format)
