from reqflow import Client, given

from reqflow.fluent_api import Given
from reqflow.assertions import equal_to, contains_string, equal_to
from reqflow.response.response import UnifiedResponse
import pytest
from unittest.mock import Mock

from httpx._exceptions import ReadTimeout

client = Client(base_url="https://httpbin.org")
mock_client = Client(base_url="http://127.0.0.1:5000")

def test_get_request():
    given(client).when("GET", "/get?foo=bar").then().status_code(200).assert_body("args.foo", equal_to("bar"))


def test_post_request():
    payload = {"foo": "bar"}
    r = given(client).body(payload).when("POST", "/post").then().status_code(200).assert_body("json.foo", equal_to("bar"))\
     .get_response()
    assert r.body.get('headers').get('Content-Type') == 'application/json'


def test_post_data_body_request():
    payload = {"foo": "bar"}
    r = given(client).body(data=payload).when("POST", "/post").then().get_response()
    assert r.body.get('headers').get('Content-Type') == 'application/x-www-form-urlencoded'


def test_post_json_body_request():
    payload = {"foo": "bar"}
    r = given(client).body(json=payload).when("POST", "/post").then().get_response()
    assert r.body.get('headers').get('Content-Type') == 'application/json'


@pytest.mark.xfail(raises=ValueError)
def test_post_both_types_body_request():
    payload = {"foo": "bar"}
    given(client).body(json=payload, data=payload).when("POST", "/post").then().get_response()


def test_status_code_404():
    given(client).when("GET", "/nonexistent").then().status_code(404)


def test_content_type():
    given(client).when("GET", "/text").then().\
        assert_header('Content-Type', equal_to('text/html'))


def test_header_exists():
    given(client).when("GET", "/get").then().assert_header_exists('Date')


@pytest.mark.xfail(raises=AssertionError)
def test_assert_header_exists_failure():
    given(client).when("GET", "/get").then().assert_header_exists('Non-Existent-Header')


def test_assert_header_exists_case_insensitivity():
    given(client).when("GET", "/get").then().assert_header_exists('date')


@pytest.mark.xfail(raises=ValueError)
def test_post_content_data_body_request():
    payload = {"foo": "bar"}
    given(client).body(payload, data=payload).when("POST", "/post").then().get_response()


@pytest.mark.xfail(raises=ValueError)
def test_post_content_json_body_request():
    payload = {"foo": "bar"}
    given(client).body(payload, data=payload).when("POST", "/post").then().get_response()


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
    response = client.send("GET", "/json")
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

@pytest.mark.skip(reason="Skip for CI tests")
def test_timeout():
    # TODO: Create fixture to run the server and setup on CI
    given(mock_client).when("GET", "/delay/2").then(timeout=2.5).status_code(200)

@pytest.mark.skip(reason="Skip for CI tests")
@pytest.mark.xfail(raises=ReadTimeout)
def test_timeout_xfailed():
    given(mock_client).when("GET", "/delay/2").then(timeout=1.9).status_code(200)

@pytest.mark.skip(reason="Skip for CI tests")
@pytest.mark.xfail(raises=ReadTimeout)
def test_timeout_very_small():
    given(mock_client).when("GET", "/delay/2").then(timeout=0.001).status_code(200)

@pytest.mark.skip(reason="Skip for CI tests")
def test_timeout_very_large():
    r = given(mock_client).when("GET", "/delay/2").then(timeout=10000).status_code(200)

@pytest.mark.skip(reason="Skip for CI tests")
@pytest.mark.xfail(raises=ReadTimeout)
def test_timeout_post_method():
    given(mock_client).body({"foo": "bar"}).when("POST", "/delay/2").then(timeout=1.9).status_code(200)


@pytest.mark.xfail(raises=AssertionError)
def test_assert_response_time_xfailed():
    given(client).when("GET", "/get?foo=bar").then().assert_response_time(0.01)

def test_get_encoding():
    enc = given(client).when("GET", "/get?foo=bar").then().get_encoding()
    assert enc == 'utf-8'