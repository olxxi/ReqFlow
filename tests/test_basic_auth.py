from reqflow.client import Client
from reqflow.fluent_api import given
from reqflow.assertions import equal_to
from reqflow.exceptions import InvalidCredentialsError

import pytest

client = Client(base_url="https://httpbin.org")


def test_basic_auth_successful():
    given(client).when("GET", "/basic-auth/user/passwd").with_auth("user", "passwd")\
        .then().status_code(200).assert_body("authenticated", equal_to(True)).assert_body("user", equal_to("user"))


def test_basic_hidden_auth_successful():
    given(client).when("GET", "/hidden-basic-auth/user/passwd").with_auth("user", "passwd")\
        .then().status_code(200).assert_body("authenticated", equal_to(True)).assert_body("user", equal_to("user"))


def test_basic_auth_unsuccessful():
    given(client).when("GET", "/basic-auth/user/passwd").then().status_code(401)


def test_basic_auth_wrong_credentials():
    given(client).when("GET", "/basic-auth/user/passwd").with_auth("wrong_user", "wrong_passwd").then().status_code(401)


def test_basic_auth_exception():
    with pytest.raises(InvalidCredentialsError):
        given(client).when("GET", "/basic-auth/user/passwd").with_auth("user", 1)