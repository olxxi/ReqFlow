from reqflow.request import Request


def test_with_params():
    request = Request("GET", "/users/1").with_params(foo="bar")
    assert request.params == {"foo": "bar"}


def test_with_headers():
    request = Request("GET", "/users/1").with_headers(Authorization="Bearer TOKEN")
    assert request.headers == {"Authorization": "Bearer TOKEN"}


def test_with_json():
    request = Request("GET", "/users/1").with_json({"key": "value"})
    assert request.json == {"key": "value"}
