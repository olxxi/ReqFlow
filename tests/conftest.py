import pytest
from reqflow.utils.logger import GlobalLogger

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    yield

@pytest.hookimpl
def pytest_sessionfinish(session, exitstatus):
    logs = GlobalLogger.get_logs()
    if logs:
        GlobalLogger.generate_html_report(file_path="test_report.html", report_title="Aggregated Requests")
        GlobalLogger.generate_json_report(file_path="test_report.json")
    GlobalLogger.clear_logs()