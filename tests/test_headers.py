from reqflow.rest.client import Client
from reqflow.rest.fluent_api import given
from httpx._models import Headers
from reqflow.rest.assertions import equal_to

client = Client(base_url="https://httpbin.org")


def test_get_headers():
    hdr = given(client).when("GET", "/get?foo=bar").then().get_headers()
    assert isinstance(hdr, Headers)


def test_get_header():
    given(client).when("GET", "/get?foo=bar")\
        .then().assert_header("Content-Type", equal_to("application/json"))
