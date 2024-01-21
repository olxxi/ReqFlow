from reqflow.response.response import UnifiedResponse
import httpx


def test_json():
    http_response = httpx.Response(200, json={"foo": "bar"})
    response = UnifiedResponse(http_response)
    assert response.json == {"foo": "bar"}


def test_text():
    http_response = httpx.Response(200, content=b"foo bar", headers={'Content-Type': 'text/plain'})
    response = UnifiedResponse(http_response)
    assert response.text == "foo bar"
