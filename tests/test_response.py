from reqflow.response.response import UnifiedResponse
import httpx
import pytest
from json.decoder import JSONDecodeError

def test_json():
    http_response = httpx.Response(200, json={"foo": "bar"})
    response = UnifiedResponse(http_response)
    assert response.json == {"foo": "bar"}


def test_text():
    http_response = httpx.Response(200, content=b"foo bar", headers={'Content-Type': 'text/plain'})
    response = UnifiedResponse(http_response)
    assert response.text == "foo bar"


def test_force_json_true():
    http_response = httpx.Response(200, content='{"key": "value"}', headers={'Content-Type': 'text/plain'})
    unified_response = UnifiedResponse(http_response, force_json=True)

    assert unified_response.body == {"key": "value"}


def test_force_json_true_decode_error():
    http_response = httpx.Response(200, content='Invalid JSON', headers={'Content-Type': 'text/plain'})

    with pytest.raises(JSONDecodeError):
        UnifiedResponse(http_response, force_json=True)