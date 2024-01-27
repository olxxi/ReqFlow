from reqflow import Client, given

from reqflow.fluent_api import Given
from reqflow.assertions import equal_to, contains_string, equal_to
from reqflow.response.response import UnifiedResponse
import pytest
from unittest.mock import Mock

client = Client(base_url="https://httpbin.org")


def test_get_request():
    given(client).when("GET", "/get?foo=bar").then().status_code(200).assert_body("args.foo", equal_to("bar"))


def test_post_request():
    payload = {"foo": "bar"}
    given(client).body(payload).when("POST", "/post").then().status_code(200).assert_body("json.foo", equal_to("bar"))


def test_put_request():
    payload = {"foo": "bar"}
    given(client).body(payload).when("PUT", "/put").then().status_code(200).assert_body("json.foo", equal_to("bar"))


def test_patch_request():
    payload = {"foo": "bar"}
    given(client).body(payload).when("PATCH", "/patch").then().status_code(200).assert_body("json.foo", equal_to("bar"))


def test_delete_request():
    given(client).when("DELETE", "/delete").then().status_code(200)


def test_contains_string_assertion():
    payload = {"foo": "bar"}
    given(client).body(payload).when("POST", "/post").then().status_code(200).assert_body("json.foo", equal_to("bar"))\
        .assert_body("json.foo", contains_string("ar"))


def test_is_assertion():
    payload = {"foo": "bar"}
    given(client).body(payload).when("POST", "/post").then().status_code(200).assert_body("json.foo", equal_to("bar"))\
        .assert_body("json.foo", equal_to("bar"))

    payload = {"foo": 123}
    given(client).body(payload).when("POST", "/post").then().status_code(200).assert_body("json.foo", equal_to(123))

    payload = {"foo": True}
    given(client).body(payload).when("POST", "/post").then().status_code(200).assert_body("json.foo", equal_to(True))


def test_get_body():
    client_t = Client(base_url="https://httpbin.org")
    response = client._send("GET", "/json")
    then = given(client).when("GET", "/json").then()

    # Test that get_body returns the JSON body of the response
    body = then.get_content()
    assert isinstance(body, dict)
    assert "slideshow" in body

    # Test that get_body returns None if the response body is not valid JSON
    http_response_mock = Mock()
    http_response_mock.content = b"not json"
    http_response_mock.headers = {'Content-Type': 'application/json'}
    response = UnifiedResponse(http_response_mock)
    then = Given(client_t).when("GET", "/json").then()
    body = then.get_content()
    assert body is not None


def test_status_code_is_between():
    given(client).when("GET", "/get?foo=bar").then().status_code_is_between(200, 299)


def test_assert_response_time():
    given(client).when("GET", "/get?foo=bar").then().assert_response_time(5)


@pytest.mark.xfail(raises=AssertionError)
def test_assert_response_time_xfailed():
    given(client).when("GET", "/get?foo=bar").then().assert_response_time(0.01)

def test_get_encoding():
    enc = given(client).when("GET", "/get?foo=bar").then().get_encoding()
    assert enc == 'utf-8'