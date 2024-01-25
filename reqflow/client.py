from typing import Any, Dict, Optional

import httpx
import time
from reqflow.response.response import UnifiedResponse


class Client:
    """
    A client for sending HTTP requests.

    Examples:
        >>> from reqflow import Client
        >>>
        >>> client = Client(base_url="https://some_url.com")

    Returns:

    """

    def __init__(self, base_url: Optional[str] = ""):
        """
        Args:
            base_url (str): The base URL for all requests sent by this client. The URL parameter is optional and can be
            overridden by the URL parameter in when() method.
        """
        self.base_url = base_url
        self.http_client = httpx.Client()

    def _send(
        self,
        method: str,
        url: str = "",
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        cookies: Optional[Dict[str, Any]] = None,
        json: Optional[Any] = None,
        redirect: Optional[bool] = False,
        files: Optional[Dict[str, Any]] = None,
    ) -> UnifiedResponse:

        start_time = time.time()
        full_url = f"{self.base_url}{url}"

        http_response = self.http_client.request(
            method, full_url, params=params, headers=headers, json=json, cookies=cookies, follow_redirects=redirect,
            files=files
        )

        response_time = time.time() - start_time

        return UnifiedResponse(http_response, response_time, response_type='REST')
