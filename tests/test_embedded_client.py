import pytest
from reqflow import given, Client
from reqflow.fluent_api import Given
from reqflow.exceptions import GivenInitializationError

def test_given_with_client():
    client = Client(base_url="https://url.com")
    result = given(client)
    assert isinstance(result, Given)

def test_given_with_url():
    result = given(url="https://url.com")
    assert isinstance(result, Given)

def test_given_with_client_and_url_raises_error():
    client = Client(base_url="https://url.com")
    with pytest.raises(GivenInitializationError):
        given(client, url="https://url.com")

def test_given_with_client_and_logging_raises_error():
    client = Client(base_url="https://url.com")
    with pytest.raises(GivenInitializationError):
        given(client, logging=True)

def test_given_without_client_or_url_raises_error():
    with pytest.raises(GivenInitializationError):
        given()