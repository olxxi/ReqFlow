from reqflow import Client
from reqflow.response.response import UnifiedResponse


def test_send_request():
    client = Client(base_url="https://jsonplaceholder.typicode.com")
    response = client.send("GET", "/users/1")
    assert isinstance(response, UnifiedResponse)
    assert response.status_code == 200
