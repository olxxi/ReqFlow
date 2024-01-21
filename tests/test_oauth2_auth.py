from reqflow import Client, given
from reqflow.assertions import equal_to


client = Client(base_url="https://httpbin.org")


def test_oauth2_successful():
    token = "some_valid_token"
    given(client).when("GET", "/bearer").with_oauth2(token)\
        .then().status_code(200).assert_body("authenticated", equal_to(True)).assert_body("token", equal_to(token))


def test_oauth2_unsuccessful():
    given(client).when("GET", "/bearer").then().status_code(401)
