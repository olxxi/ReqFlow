import pytest

from reqflow import Client, given
from reqflow.assertions import equal_to

client = Client(base_url="https://httpbin.org")


def test_set_cookies():
    cks = {"cookie1": "value1", "cookie2": "value2"}
    given(client).cookies(cks).when("GET", "/cookies").then().assert_body("cookies", equal_to(cks))


def test_get_cookie():
    r = given(client).query_param('chocolate', 'chip').when("GET", "/cookies/set").then().get_cookies()
    assert r['chocolate'] == 'chip'


def test_assert_cookie():
    given(client).query_param('chocolate', 'chip').when("GET", "/cookies/set").then()\
        .assert_cookie('chocolate', equal_to('chip'))