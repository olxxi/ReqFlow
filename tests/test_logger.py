import pytest
from reqflow.utils.logger import GlobalLogger
from reqflow import Client, given


def test_log_request():
    log_entry = {
        'function': 'test_func',
        'request': {
            'method': 'GET',
            'url': 'https://example.com',
            'params': {},
            'headers': {},
            'cookies': {},
            'json': None,
            'data': None,
            'redirect': False,
            'files': {},
            'timeout': 5.0,
        },
        'response': {
            'status_code': 200,
            'headers': {'Content-Type': 'application/json'},
            'content': b'{"key": "value"}',
            'time': 0.123,
        }
    }

    GlobalLogger.log_request(log_entry)
    logs = GlobalLogger.get_logs()
    assert len(logs) == 1
    assert logs[0]['function'] == 'test_func'
    assert logs[0]['response']['status_code'] == 200
    GlobalLogger.clear_logs()

def test_clear_logs():
    log_entry = {
        'function': 'test_func',
        'request': {
            'method': 'GET',
            'url': 'https://example.com',
            'params': {},
            'headers': {},
            'cookies': {},
            'json': None,
            'data': None,
            'redirect': False,
            'files': {},
            'timeout': 5.0,
        },
        'response': {
            'status_code': 200,
            'headers': {'Content-Type': 'application/json'},
            'content': b'{"key": "value"}',
            'time': 0.123,
        }
    }

    GlobalLogger.log_request(log_entry)
    GlobalLogger.clear_logs()
    logs = GlobalLogger.get_logs()
    assert len(logs) == 0

def test_generate_json_report(tmp_path):
    log_entry = {
        'function': 'test_func',
        'request': {
            'method': 'GET',
            'url': 'https://example.com',
            'params': {},
            'headers': {},
            'cookies': {},
            'json': None,
            'data': None,
            'redirect': False,
            'files': {},
            'timeout': 5.0,
        },
        'response': {
            'status_code': 200,
            'headers': {'Content-Type': 'application/json'},
            'content': b'{"key": "value"}',
            'time': 0.123,
        }
    }

    GlobalLogger.log_request(log_entry)
    report_path = tmp_path / "test_report.json"
    GlobalLogger.generate_json_report(file_path=str(report_path))

    with open(report_path, "r") as file:
        data = file.read()
        assert '"function": "test_func"' in data
        assert '"status_code": 200' in data
    GlobalLogger.clear_logs()


def test_generate_html_report(tmp_path):
    log_entry = {
        'function': 'test_func',
        'request': {
            'method': 'GET',
            'url': 'https://example.com',
            'params': {},
            'headers': {},
            'cookies': {},
            'json': None,
            'data': None,
            'redirect': False,
            'files': {},
            'timeout': 5.0,
        },
        'response': {
            'status_code': 200,
            'headers': {'Content-Type': 'application/json'},
            'content': b'{"key": "value"}',
            'time': 0.123,
        }
    }

    GlobalLogger.log_request(log_entry)
    report_path = tmp_path / "test_report.html"
    GlobalLogger.generate_html_report(file_path=str(report_path))

    with open(report_path, "r") as file:
        data = file.read()
        assert "<h1>Test Report" in data
        assert "test_func" in data
        assert "example.com" in data
        GlobalLogger.clear_logs()


def test_client_logger():
    client = Client(base_url="https://httpbin.org", logging=True)

    given(client).when("GET", "/get?foo=bar").then().status_code(200)

    logs = GlobalLogger.get_logs()
    assert len(logs) == 1
    assert logs[0]['function'] == 'test_client_logger'

    payload = {"foo": "bar"}
    given(client).body(data=payload).when("POST", "/post").then().status_code(200)

    logs = GlobalLogger.get_logs()
    assert len(logs) == 2

if __name__ == "__main__":
    pytest.main()
