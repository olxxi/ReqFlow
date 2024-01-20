# src/reqflow/_graphql/fluent.py

from .client import ClientGraph
from .request import GraphQLRequest
from reqflow.response.response import UnifiedResponse
from reqflow.validator.validator import Validator
from typing import Any
from pydantic import BaseModel
from pydantic import ValidationError


def given_graphql(client: ClientGraph):
    return GivenGraphQL(client)


class GivenGraphQL:
    def __init__(self, client: ClientGraph):
        self.client = client
        self.variables_dict = {}
        self.operation_text = ""
        self.is_mutation = False

    def query(self, query: str):  # Method to set the query string
        self.operation_text = query
        self.is_mutation = False
        return self

    def mutation(self, mutation: str):
        self.operation_text = mutation
        self.is_mutation = True
        return self

    def variables(self, variables: dict):
        self.variables_dict = variables
        return self

    def when(self):
        return WhenGraphQL(self.client, self.operation_text, self.variables_dict, self.is_mutation)


class WhenGraphQL:
    def __init__(self, client: ClientGraph, operation: str, variables: dict, is_mutation: bool):
        self.client = client
        self.operation = operation
        self.variables = variables
        self.is_mutation = is_mutation

    def then(self) -> 'ThenGraphQL':
        request = GraphQLRequest(operation=self.operation, variables=self.variables, is_mutation=self.is_mutation)
        response = self.client.send(request)
        return ThenGraphQL(response)


class ThenGraphQL:
    def __init__(self, response: UnifiedResponse):
        self.response = response

    def get_response(self):
        return self.response

    def status_code(self, expected_status_code: int):
        assert self.response.status_code == expected_status_code, \
            f"Status code {self.response.status_code} is not {expected_status_code}"
        return self

    def expecting_data(self, expected_data: Any):
        assert self.response.content == expected_data, \
            "The returned data does not match the expected data"
        return self

    def errors(self, expected_errors: Any):
        assert self.response.errors == expected_errors, \
            "The returned errors do not match the expected errors"
        return self

    # TODO tests
    def validate_data(self, expected_model: BaseModel):
        validator = Validator(model=expected_model)
        try:
            validator.validate(self.response.content)
        except ValidationError as e:
            raise AssertionError(f"The response data does not match the expected model: {str(e)}")
        return self

    def assert_response_time(self, max_time: float):
        assert self.response.response_time <= max_time, \
            f"Response time {self.response.response_time} exceeds the maximum expected time {max_time}"
        return self

