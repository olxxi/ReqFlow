from pydantic import BaseModel
import pytest

from reqflow import given, Client
from reqflow.exceptions import ValidationError

client = Client(base_url="https://httpbin.org")


class TestModelValid(BaseModel):
    args: dict
    data: str
    files: dict
    form: dict
    headers: dict
    json: dict
    origin: str
    url: str


class TestModelInvalid(BaseModel):
    args: dict
    data: str
    files: dict
    form: dict
    headers: dict
    json: str
    origin: str


def test_validate_valid():
    payload = {"foo": "bar"}
    given(client).body(payload).when("POST", "/post").then().status_code(200).validate_data(TestModelValid)


@pytest.mark.xfail(raises=AssertionError)
def test_validate_invalid():
    payload = {"foo": "bar"}
    given(client).body(payload).when("POST", "/post").then().status_code(200).validate_data(TestModelInvalid)
