import asyncio

import pytest

from reqflow import Client, given
from reqflow.assertions import equal_to, contains_string


@pytest.mark.asyncio
async def test_get_request_async():
    client = Client(base_url="https://httpbin.org")
    result = await given(client).when("GET", "/get?foo=bar").then_async()

    result.status_code(200).assert_body("args.foo", equal_to("bar"))


@pytest.mark.asyncio
async def test_get_request_with_context_manager_async():
    async with Client(base_url="https://httpbin.org") as client:
        result = await given(client).when("GET", "/get?foo=bar").then_async()
        result.status_code(200).assert_body("args.foo", equal_to("bar"))


@pytest.mark.asyncio
async def test_post_request_async():
    client = Client(base_url="https://httpbin.org")
    payload = {"foo": "bar"}
    result = await given(client).body(payload).when("POST", "/post").then_async()

    result.status_code(200).assert_body("json.foo", equal_to("bar"))


@pytest.mark.asyncio
async def test_post_request_with_context_manager_async():
    async with Client(base_url="https://httpbin.org") as client:
        payload = {"foo": "bar"}
        result = await given(client).body(payload).when("POST", "/post").then_async()
        result.status_code(200).assert_body("json.foo", equal_to("bar"))


@pytest.mark.asyncio
async def test_post_data_body_request_async():
    client = Client(base_url="https://httpbin.org")
    payload = {"foo": "bar"}
    result = await given(client).body(data=payload).when("POST", "/post").then_async()
    assert result.get_response().body.get('headers').get('Content-Type') == 'application/x-www-form-urlencoded'


@pytest.mark.asyncio
async def test_post_json_body_request_async():
    client = Client(base_url="https://httpbin.org")
    payload = {"foo": "bar"}
    result = await given(client).body(json=payload).when("POST", "/post").then_async()
    assert result.get_response().body.get('headers').get('Content-Type') == 'application/json'


@pytest.mark.asyncio
async def test_put_request_async():
    client = Client(base_url="https://httpbin.org")
    payload = {"foo": "bar"}
    result = await given(client).body(payload).when("PUT", "/put").then_async()
    result.status_code(200).assert_body("json.foo", equal_to("bar"))


@pytest.mark.asyncio
async def test_patch_request_async():
    client = Client(base_url="https://httpbin.org")
    payload = {"foo": "bar"}
    result = await given(client).body(payload).when("PATCH", "/patch").then_async()
    result.status_code(200).assert_body("json.foo", equal_to("bar"))


@pytest.mark.asyncio
async def test_delete_request_async():
    client = Client(base_url="https://httpbin.org")
    result = await given(client).when("DELETE", "/delete").then_async()
    result.status_code(200)


@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint, query_params", [
    ("/get", {"test": "value1"}),
    ("/ip", {"test": "value2"}),
    ("/user-agent", {"test": "value3"})
])
async def test_async_parametrized(endpoint, query_params):
    client = Client(base_url="https://httpbin.org")
    result = await given(client).query_param(query_params).when("GET", endpoint).then_async()
    result.status_code(200)


@pytest.mark.asyncio
async def test_multiple_async_requests():
    client = Client(base_url="https://httpbin.org")
    tasks = [
        given(client).query_param({"test": "value1"}).when("GET", "/get").then_async(),
        given(client).query_param({"test": "value2"}).when("GET", "/ip").then_async(),
        given(client).query_param({"test": "value3"}).when("GET", "/user-agent").then_async()
    ]

    results = await asyncio.gather(*tasks)

    for result in results:
        result.status_code(200)



@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint, query_params", [
    ("/get", {"test": "value1"}),
    ("/ip", {"test": "value2"}),
    ("/user-agent", {"test": "value3"})
])
async def test_async_parametrized_with_context_manager(endpoint, query_params):
    async with Client(base_url="https://httpbin.org") as client:
        result = await given(client).query_param(query_params).when("GET", endpoint).then_async()
        result.status_code(200)


@pytest.mark.asyncio
async def test_assertions_async():
    client = Client(base_url="https://httpbin.org")
    payload = {"foo": "bar"}
    result = await given(client).body(payload).when("POST", "/post").then_async()
    result.status_code(200).assert_body("json.foo", equal_to("bar")).\
        assert_body("json.foo", contains_string("ar"))


@pytest.mark.asyncio
async def test_assert_response_time_async():
    client = Client(base_url="https://httpbin.org")
    result = await given(client).when("GET", "/get?foo=bar").then_async()
    result.assert_response_time(5)


@pytest.mark.asyncio
async def test_assert_header_async():
    client = Client(base_url="https://httpbin.org")
    result = await given(client).when("GET", "/get").then_async()
    result.assert_header('Content-Type', equal_to('application/json'))


@pytest.mark.asyncio
async def test_status_code_is_between_async():
    client = Client(base_url="https://httpbin.org")
    result = await given(client).when("GET", "/get?foo=bar").then_async()
    result.status_code_is_between(200, 299)


@pytest.mark.asyncio
async def test_get_request_async_embedded_client():
    result = await given(url="https://httpbin.org").when("GET", "/get?foo=bar").then_async()

    result.status_code(200).assert_body("args.foo", equal_to("bar"))


@pytest.mark.asyncio
async def test_post_request_async_embedded_client():
    payload = {"foo": "bar"}
    result = await given(url="https://httpbin.org").body(payload).when("POST", "/post").then_async()

    result.status_code(200).assert_body("json.foo", equal_to("bar"))


@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint, query_params", [
    ("/get", {"test": "value1"}),
    ("/ip", {"test": "value2"}),
    ("/user-agent", {"test": "value3"})
])
async def test_async_parametrized_embedded_client(endpoint, query_params):
    result = await given(url="https://httpbin.org").query_param(query_params).when("GET", endpoint).then_async()
    result.status_code(200)


@pytest.mark.asyncio
async def test_assertions_async_embedded_client():
    payload = {"foo": "bar"}
    result = await given(url="https://httpbin.org").body(payload).when("POST", "/post").then_async()
    result.status_code(200).assert_body("json.foo", equal_to("bar")).\
        assert_body("json.foo", contains_string("ar"))


@pytest.mark.asyncio
async def test_assert_header_async_embedded_client():
    result = await given(url="https://httpbin.org").when("GET", "/get").then_async()
    result.assert_header('Content-Type', equal_to('application/json'))


@pytest.mark.asyncio
async def test_async_file_upload():
    tasks = [
        given(url="https://ps.uci.edu/~franklin").file_upload("userfile", "data/test.png").when("POST", "/doc/file_upload.html").then_async(timeout=10)
        for _ in range(5)
    ]

    results = await asyncio.gather(*tasks)

    for result in results:
        result.status_code(200)