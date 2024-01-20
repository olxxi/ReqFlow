from reqflow._graphql.client import ClientGraph
from reqflow._graphql.fluent_api_graphql import given_graphql
import pytest


client = ClientGraph("https://spacex-production.up.railway.app/")


def test_given_query():
    given = given_graphql(client).query("query ExampleQuery {company {ceo}roadster{apoapsis_au}}")

    assert given.operation_text == "query ExampleQuery {company {ceo}roadster{apoapsis_au}}"


def test_variables():
    QUERY_VARIABLES = """
    query testQuery($var: ID!) {
      cart(id: $var) {
        totalUniqueItems
        items {
          name
          unitTotal {
            amount
            formatted
          }
        }
      }
    }
    """

    client = ClientGraph("https://api.cartql.com/")

    resp = given_graphql(client).query(QUERY_VARIABLES).variables({"var": "1"}).when().then().get_response()

    assert resp.status_code == 200
    assert resp.content["cart"]["totalUniqueItems"] == 1


def test_query():
    given_graphql(client).query("query ExampleQuery {company {ceo}roadster{apoapsis_au}}") \
        .when() \
        .then().status_code(200)


def test_get_response():
    response = given_graphql(client).query("query ExampleQuery {company {ceo}roadster{apoapsis_au}}") \
        .when() \
        .then().get_response()

    assert response.status_code == 200
    assert type(response.content) == dict
    assert type(response.body) == dict
    assert response.content["company"]["ceo"] == "Elon Musk"
    assert response.errors is None


def test_data():
    given_graphql(client).query("query ExampleQuery {company {ceo}roadster{apoapsis_au}}") \
        .when() \
        .then().expecting_data({'company': {'ceo': 'Elon Musk'}, 'roadster': {'apoapsis_au': 1.664332332453025}})


def test_mutations():
    client = ClientGraph("https://api.cartql.com/")

    mutation = """
        mutation AddItem($input: AddToCartInput!) {
          addItem(input: $input) {
            id
            totalItems
            totalUniqueItems
            items {
              id
              name
              quantity
            }
            subTotal {
              amount
              currency {
                code
              }
            }
          }
        }
    """

    variables = """{
        "input": {
            "cartId": "1",
            "id": "1",
            "name": "Test Item",
            "description": "A test item description",
            "type": "SKU",
            "images": ["https://example.com/image.png"],
            "price": 1000,
            "currency": {
                "code": "USD"
            },
            "quantity": 1,
            "attributes": [],
            "metadata": {}
        }
    }"""

    resp = given_graphql(client).mutation(mutation).variables(variables).when().then().get_response()

    assert resp.status_code == 200, resp.errors
    assert resp.content["addItem"]["totalUniqueItems"] != 0, resp.errors
    assert resp.errors is None, resp.errors


@pytest.mark.xfail(raises=ValueError)
def test_mutation_err():
    client = ClientGraph("https://api.cartql.com/")
    mutation = ""
    variables = ""

    resp = given_graphql(client).mutation(mutation).variables(variables).when().then().get_response()


@pytest.mark.xfail(raises=AssertionError)
def test_assert_response_max_time_failed():
    given_graphql(client).query("query ExampleQuery {company {ceo}roadster{apoapsis_au}}") \
        .when() \
        .then().assert_response_time(0.1)


def test_assert_response_max_time():
    given_graphql(client).query("query ExampleQuery {company {ceo}roadster{apoapsis_au}}") \
        .when() \
        .then().assert_response_time(3)


def test_validate_response():
    from pydantic import BaseModel
    from typing import Optional

    class Company(BaseModel):
        ceo: str

    class Roadster(BaseModel):
        apoapsis_au: Optional[float]

    class SpaceData(BaseModel):
        company: Company
        roadster: Roadster

    given_graphql(client).query("query ExampleQuery {company {ceo}roadster{apoapsis_au}}") \
        .when() \
        .then().validate_data(expected_model=SpaceData)


@pytest.mark.xfail(raises=AssertionError)
def test_validate_response_failed():
    from pydantic import BaseModel
    from typing import Optional

    class Company(BaseModel):
        ceo: dict

    class Roadster(BaseModel):
        apoapsis_au: Optional[float]

    class SpaceData(BaseModel):
        company: Company
        roadster: Roadster

    given_graphql(client).query("query ExampleQuery {company {ceo}roadster{apoapsis_au}}") \
        .when() \
        .then().validate_data(expected_model=SpaceData)