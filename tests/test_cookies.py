import pytest

from reqflow import Client, given

client = Client(base_url="https://httpbin.org")


@pytest.mark.skip(reason="Not implemented yet")
def test_get_cookies():
    cks = given(client).when("GET", "/cookies/set").then().get_cookies()
    assert isinstance(cks, dict)

