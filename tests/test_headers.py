import pytest

from reqflow import Client, given
from httpx._models import Headers
from reqflow.assertions import equal_to
from reqflow.exceptions import InvalidArgumentError

client = Client(base_url="https://httpbin.org")


def test_get_headers():
    hdr = given(client).when("GET", "/get?foo=bar").then().get_headers()
    assert isinstance(hdr, Headers)


def test_get_headers_exception():
    with pytest.raises(InvalidArgumentError):
        given(client).headers("invalid")


def test_get_header():
    given(client).when("GET", "/get?foo=bar")\
        .then().assert_header("Content-Type", equal_to("application/json"))


def test_get_header_exception():
    with pytest.raises(InvalidArgumentError):
        given(client).header(1, 1)


def test_request_header():
    given(client).header("Authorization", "Bearer TOKEN").when("GET", "/headers")\
        .then().assert_body("headers.Authorization", equal_to("Bearer TOKEN"))


def test_request_headers():
    given(client).headers(
            {'Authorization': 'Bearer TOKEN',
             'test_header': 'test_value'})\
        .when("GET", "/headers")\
        .then()\
        .assert_body("headers.Authorization", equal_to("Bearer TOKEN"))\
        .assert_body("headers.Test-Header", equal_to("test_value"))
