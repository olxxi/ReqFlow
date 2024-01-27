# ReqFlow

ReqFlow is a Python library designed for efficient and intuitive API testing. 
ReqFlow offers a fluent and flexible interface for crafting and validating HTTP requests, 
making API testing both straightforward and adaptable. While it make sense to use standard approaches for a Python API
testing, ReqFlow reduces the entry barrier for beginners and allows for more advanced use cases with RestAssured-like
approach. 

### Features

* Fluent API for building and sending HTTP requests.
* Supports response handling and validations.
* Customizable response validation using `PyDantic` models.
* Convenient utility methods for common assertions and response manipulations.

The tool is still in development, braking changes are possible. Any feedback and contributions are highly appreciated.

### Installation

Install ReqFlow using `pip`:

```shell
pip install reqflow
```

### Quick Start

```python
from reqflow import given, Client
from pydantic import BaseModel


# Define a Pydantic model for response validation
class ExampleModel(BaseModel):
    name: str
    value: int


# Initialize the client
client = Client(base_url="https://api.example.com")

# Use ReqFlow's fluent API
response = (given(client)
            .header("Authorization", "Bearer your_token")
            .query_param("param", "value")
            .when("GET", "/your_endpoint")
            .then()
            .validate_data(ExampleModel)
            .status_code(200)
            .get_content())

print(response)
```