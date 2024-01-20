import httpx
from .request import GraphQLRequest
from reqflow.response.response import UnifiedResponse
import time


class ClientGraph:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.http_client = httpx.Client()

    def send(self, request: GraphQLRequest) -> UnifiedResponse:
        # Send the request using the httpx client
        start_time = time.time()
        # TODO: Add support for headers, and not use base url
        http_response = self.http_client.post(self.base_url, json=request.payload)
        end_time = time.time()

        response_time = end_time - start_time

        return UnifiedResponse(http_response, response_time, response_type='GRAPHQL')
