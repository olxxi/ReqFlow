from reqflow import Client, given
from reqflow.assertions import is_


client = Client(base_url="https://httpbin.org")


def test_oauth2_successful():
    token = "some_valid_token"
    given(client).when("GET", "/bearer").with_oauth2(token)\
        .then().status_code(200).body("authenticated", is_(True)).body("token", is_(token))


def test_oauth2_unsuccessful():
    given(client).when("GET", "/bearer").then().status_code(401)
