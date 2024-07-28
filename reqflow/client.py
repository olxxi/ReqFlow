from typing import Any, Dict, Optional, Union

import httpx
import time
from reqflow.response.response import UnifiedResponse
from reqflow.utils.logger import GlobalLogger
import inspect

class Client:
    """
    A client for sending HTTP requests.

    Examples:
        >>> from reqflow import Client
        >>>
        >>> client = Client(base_url="https://some_url.com")

    """

    def __init__(self, base_url: Optional[str] = "", logging: Optional[bool] = False):
        """
        Args:
            base_url (str): The base URL for all requests sent by this client. The URL parameter is optional and can be overridden by the URL parameter in when() method.
            logging (bool): If True, logs will be stored for each request sent by this client.
        """
        self.base_url = base_url
        self.logging = logging
        self.http_client = httpx.Client()
        self.async_http_client = httpx.AsyncClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.async_http_client.aclose()
        self.http_client.close()

    @staticmethod
    def _log_request(called_function, method, url, params, headers, cookies, json, data,
                    redirect, files, timeout, response, response_time):
        log_entry = {
            'function': called_function,
            'request': {
                'method': method,
                'url': url,
                'params': params,
                'headers': headers,
                'cookies': cookies,
                'json': json,
                'data': data,
                'redirect': redirect,
                'files': files,
                'timeout': timeout
            },
            'response': {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content': response.content,
                'time': response_time
            }
        }

        GlobalLogger.log_request(log_entry)

    @staticmethod
    def _get_caller() -> Union[str, None]:
        try:
            current_frame = inspect.currentframe()
            return inspect.getouterframes(current_frame)[4].__getattribute__('function')
        except IndexError:
            return None

    def _add_to_log(self, method, url, params, headers, cookies, json, data,
                    redirect, files, timeout, response, response_time) -> None:
        called_function = self._get_caller()
        self._log_request(called_function, method, url, params, headers, cookies, json,
                             data, redirect, files, timeout, response, response_time)

    def send(
        self,
        method: str,
        url: str = "",
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        cookies: Optional[Dict[str, Any]] = None,
        json: Optional[Any] = None,
        data: Optional[Any] = None,
        redirect: Optional[bool] = False,
        files: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = 5.0,
        force_json: Optional[bool] = False
    ) -> UnifiedResponse:

        start_time = time.time()
        full_url = f"{self.base_url}{url}"

        http_response = self.http_client.request(
            method, full_url, params=params, headers=headers, json=json, data=data,cookies=cookies,
            follow_redirects=redirect, files=files, timeout=timeout
        )

        response_time = time.time() - start_time

        if self.logging:
            self._add_to_log(method, full_url, params, headers, cookies, json,
                             data, redirect, files, timeout, http_response, response_time)


        return UnifiedResponse(http_response, response_time, response_type='REST', force_json=force_json)

    async def send_async(
        self,
        method: str,
        url: str = "",
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        cookies: Optional[Dict[str, Any]] = None,
        json: Optional[Any] = None,
        data: Optional[Any] = None,
        redirect: Optional[bool] = False,
        files: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = 5.0,
        force_json: Optional[bool] = False
    ) -> UnifiedResponse:

        start_time = time.time()
        full_url = f"{self.base_url}{url}"

        http_response = await self.async_http_client.request(
            method, full_url, params=params, headers=headers, json=json, data=data,cookies=cookies,
            follow_redirects=redirect, files=files, timeout=timeout
        )

        response_time = time.time() - start_time

        if self.logging:
            self._add_to_log(method, full_url, params, headers, cookies, json,
                             data, redirect, files, timeout, http_response, response_time)

        return UnifiedResponse(http_response, response_time, response_type='REST', force_json=force_json)
