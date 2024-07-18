from pydantic import BaseModel, Field, constr, condecimal
import pytest

from reqflow import given

class GeoValid(BaseModel):
    lat: float = Field(gt=-90.0, lt=90.0)
    lng: float = Field(gt=-180.0, lt=180.0)

class AddressValid(BaseModel):
    street: str = Field(min_length=1, max_length=100)
    suite: str = Field(min_length=1, max_length=100)
    city: str = Field(min_length=1, max_length=100)
    zipcode: str = Field(min_length=5, max_length=10)
    geo: GeoValid

class CompanyValid(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    catchPhrase: str = Field(min_length=1, max_length=255)
    bs: str = Field(min_length=1, max_length=255)

class UserValid(BaseModel):
    id: int = Field(default=1, validate_default=True)
    name: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=100)
    address: AddressValid
    phone: str = Field(min_length=10, max_length=30)
    website: str = Field(min_length=1, max_length=100)
    company: CompanyValid


class GeoInvalid(BaseModel):
    lat: float = Field(gt=-30.0, lt=90.0)
    lng: float = Field(gt=-180.0, lt=180.0)

class AddressInvalid(BaseModel):
    street: str = Field(min_length=1, max_length=2)
    suite: str = Field(min_length=1, max_length=100)
    city: str = Field(min_length=1, max_length=100)
    zipcode: str = Field(min_length=5, max_length=10)
    geo: GeoInvalid

class CompanyInvalid(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    catchPhrase: str = Field(min_length=1, max_length=255)
    bs: str = Field(min_length=1, max_length=255)

class UserInvalid(BaseModel):
    id: int = Field(default=3, validate_default=True)
    name: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=100)
    address: AddressInvalid
    phone: str = Field(min_length=10, max_length=30)
    website: str = Field(min_length=1, max_length=100)
    company: CompanyInvalid


def test_validator_constraints():
    given(url="https://jsonplaceholder.typicode.com/users/1")\
        .when("GET").then()\
        .validate_data(UserValid)


def test_validator_float_xfail():
    with pytest.raises(AssertionError):
        given(url="https://jsonplaceholder.typicode.com/users/1")\
            .when("GET").then()\
            .validate_data(UserInvalid)
