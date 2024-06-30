from reqflow.utils.constants import HTML_TEMPLATE
from datetime import datetime
import json

class GlobalLogger:
    """
    A global logger to store all the requests made by the client.
    """
    logs = []

    @classmethod
    def log_request(cls, log):
        """
        Add a log entry to the logs list.
        Args:
            log: A dictionary containing the log entry.
        """

        cls.logs.append(log)

    @classmethod
    def get_logs(cls):
        """
        Get all the logs stored in the logger.
        Returns:
            A list of log entries.

        Examples:
            >>> from reqflow.utils.logger import GlobalLogger
            >>>
            >>> logs = GlobalLogger.get_logs()
            >>> print(logs)
            >>> [{'function': 'test_function', 'request': {'method': 'GET', 'url': 'https://some_url.com', 'params': {}, 'headers': {}, 'cookies': {}, 'json': None, 'data': None, 'redirect': 'auto', 'files': None, 'timeout': None}, 'response': {'status_code': 200, 'headers': {'Content-Type': 'application/json'}, 'content': b'{"key": "value"}', 'time': 0.123}}]
        """

        return cls.logs

    @classmethod
    def clear_logs(cls):
        """
        Clear all the logs stored in the logger.

        Examples:
            >>> from reqflow.utils.logger import GlobalLogger
            >>>
            >>> GlobalLogger.clear_logs()
        """

        cls.logs.clear()

    @classmethod
    def generate_html_report(cls, file_path="test_report.html", report_title="Test Report"):
        """
        Generate an HTML report from the logs across all client instances.
        Args:
            file_path: (str) The path/name to save the HTML report.
            report_title: (str) The name of the report.

        Examples:
            >>> from reqflow.utils.logger import GlobalLogger
            >>>
            >>> GlobalLogger.generate_html_report(file_path="test_report.html", report_title="Aggregated Requests")

        """

        log_entries = ""
        for log in cls.logs:
            log_entries += f"""
            <div class="log">
                <div class="log-header" onclick="toggleLog(this)">
                    {log['function']} - Status: <span class="{'status-success' if log['response']['status_code'] < 300 else 'status-failure'}"><b>{log['response']['status_code']}</b></span>
                </div>
                <div class="log-body">
                    <h3>Request</h3>
                    <table>
                        <tr><th>Method</th><td>{log['request']['method']}</td></tr>
                        <tr><th>URL</th><td>{log['request']['url']}</td></tr>
                        <tr><th>Params</th><td>{log['request']['params']}</td></tr>
                        <tr><th>Headers</th><td>{log['request']['headers']}</td></tr>
                        <tr><th>Cookies</th><td>{log['request']['cookies']}</td></tr>
                        <tr><th>JSON</th><td>{log['request']['json']}</td></tr>
                        <tr><th>Data</th><td>{log['request']['data']}</td></tr>
                        <tr><th>Redirect</th><td>{log['request']['redirect']}</td></tr>
                        <tr><th>Files</th><td>{log['request']['files']}</td></tr>
                        <tr><th>Timeout</th><td>{log['request']['timeout']}</td></tr>
                    </table>
                    <h3>Response</h3>
                    <table>
                        <tr><th>Status Code</th><td>{log['response']['status_code']}</td></tr>
                        <tr><th>Headers</th><td>{log['response']['headers']}</td></tr>
                        <tr><th>Content</th><td>{log['response']['content']}</td></tr>
                        <tr><th>Time</th><td>{log['response']['time']}</td></tr>
                    </table>
                </div>
            </div>
            """

        html_content = HTML_TEMPLATE.format(log_entries=log_entries, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                            report_name=report_title)

        with open(file_path, "w") as file:
            file.write(html_content)

    @classmethod
    def generate_json_report(cls, file_path="test_report.json"):
        """
        Generate a JSON report from the logs across all client instances.
        Args:
            file_path: (str) The path/name to save the HTML report.

        Examples:
            >>> from reqflow.utils.logger import GlobalLogger
            >>>
            >>> GlobalLogger.generate_json_report(file_path="test_report.json")
        """

        def convert_bytes(o):
            if isinstance(o, bytes):
                return o.decode("utf-8")
            raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

        with open(file_path, "w") as file:
            json.dump(cls.logs, file, default=convert_bytes, indent=4)
