from typing import Any, Dict, Optional

import httpx
import time
from reqflow.response.response import UnifiedResponse


class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.http_client = httpx.Client()

    def send(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        json: Optional[Any] = None,
    ) -> UnifiedResponse:
        start_time = time.time()
        full_url = f"{self.base_url}{url}"
        http_response = self.http_client.request(
            method, full_url, params=params, headers=headers, json=json
        )

        response_time = time.time() - start_time

        return UnifiedResponse(http_response, response_time, response_type='REST')
