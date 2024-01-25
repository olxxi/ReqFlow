from reqflow import given, Client
from reqflow.assertions import *

import pytest

client = Client(base_url="https://httpbin.org")

payload = {
    'string': 'some long string',
    'float': 1.123,
    'integer': 100,
    'boolean': True,
    'list_int': [1, 2, 3],
    'list_str': ['a', 'b', 'c'],
    'list_bool': [True, False, True],
    'none': None,
    'regex': 'abc123'
}


def test_contains_string():
    given(client).body(payload).when('POST', "/post").then().assert_body('json.string', contains_string('long'))


def test_equal_to():
    given(client).body(payload).when('POST', "/post").then().assert_body('json.float', equal_to(1.123))\
        .assert_body('json.integer', equal_to(100)) \
        .assert_body('json.boolean', equal_to(True))\
        .assert_body('json.list_int', equal_to([1, 2, 3]))\
        .assert_body('json.list_str', equal_to(['a', 'b', 'c']))\
        .assert_body('json.list_bool', equal_to([True, False, True]))\
        .assert_body('json.none', equal_to(None))\
        .assert_body('json.regex', equal_to('abc123'))


def test_not_equal_to():
    given(client).body(payload).when('POST', "/post").then().assert_body('json.float', not_equal_to(1.12))\
        .assert_body('json.integer', not_equal_to(101)) \
        .assert_body('json.boolean', not_equal_to(False))\
        .assert_body('json.list_int', not_equal_to([1, 2, 4]))\
        .assert_body('json.list_str', not_equal_to(['a', 'b', 'd']))\
        .assert_body('json.list_bool', not_equal_to([True, False, False]))\
        .assert_body('json.none', not_equal_to('not_none'))\
        .assert_body('json.regex', not_equal_to('abc1234'))


def test_greater_than():
    given(client).body(payload).when('POST', "/post").then().assert_body('json.float', greater_than(1.12))\
        .assert_body('json.integer', greater_than(99)) \
        .assert_body('json.regex', greater_than('abc122'))


def test_greater_less_then():
    given(client).body(payload).when('POST', "/post").then()\
        .assert_body('json.float', less_than(1.124))\
        .assert_body('json.integer', less_than(101)) \
        .assert_body('json.regex', less_than('abc124'))


def test_contains_in_list():
    given(client).body(payload).when('POST', "/post").then().assert_body('json.list_int', list_contains(1))\
        .assert_body('json.list_str', list_contains('a')) \
        .assert_body('json.list_bool', list_contains(True))


def test_is_none():
    given(client).body(payload).when('POST', "/post").then().assert_body('json.none', is_none())


def test_is_not_none():
    given(client).body(payload).when('POST', "/post").then().assert_body('json.string', is_not_none())


def test_matches_regex():
    given(client).body(payload).when('POST', "/post").then().assert_body('json.regex', matches_regex('abc123'))


def test_combined_assertions_and_or():
    given(client).body(payload).when('POST', "/post").then() \
        .assert_body('json.float', or_(less_than(1.124), equal_to(2))) \
        .assert_body('json.float', and_(less_than(1.124), greater_than(1)))


@pytest.mark.xfail(raises=AssertionError)
def test_combined_assertions_or_failed():
    given(client).body(payload).when('POST', "/post").then() \
        .assert_body('json.float', or_(less_than(1), equal_to(2))) \
        .assert_body('json.float', and_(less_than(1.124), greater_than(1)))


@pytest.mark.xfail(raises=AssertionError)
def test_combined_assertions_and_failed():
    given(client).body(payload).when('POST', "/post").then() \
        .assert_body('json.float', and_(less_than(1), greater_than(1)))