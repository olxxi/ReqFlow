from reqflow import Client, given
from reqflow.response.response import UnifiedResponse
from reqflow.assertions import equal_to


def test_send_request():
    client = Client(base_url="https://jsonplaceholder.typicode.com")
    response = client.send("GET", "/users/1")
    assert isinstance(response, UnifiedResponse)
    assert response.status_code == 200


def test_client_redirect_true():
    client = Client(base_url="https://httpbin.org")
    given(client).when("GET", "/redirect/1").then(follow_redirects=True)\
        .assert_body("url", equal_to("https://httpbin.org/get")).status_code(200)


def test_client_redirect_false():
    client = Client(base_url="https://httpbin.org")
    given(client).when("GET", "/redirect/1").then().status_code(302)
