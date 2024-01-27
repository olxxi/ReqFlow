import re


def contains_string(expected):
    """
    Asserts that the actual value contains the provided string.

    Args:
        expected: The string to check for in the actual value.

    Examples:
        >>> from reqflow import Client, given
        >>> from reqflow.assertions import contains_string
        >>> client = Client(base_url="https://httpbin.org")
        >>> given(client).when("GET", "/get?foo=bar").then().assert_body("url", contains_string("foo=bar"))

    Returns:
        An assertion function that checks if the actual value contains the provided string.
    """
    def assertion(actual):
        assert expected in actual, f"Expected '{actual}' to contain string '{expected}'"
    return assertion


def equal_to(expected):
    """
    Asserts that the actual value is equal to the provided value.

    Args:
        expected: The value to check for equality against the actual value.

    Examples:
        >>> from reqflow import Client, given
        >>> from reqflow.assertions import equal_to
        >>> client = Client(base_url="https://httpbin.org")
        >>> given(client).when("GET", "/get?foo=bar").then().assert_body("url", equal_to("https://httpbin.org/get?foo=bar"))

    Returns:
        An assertion function that checks if the actual value is equal to the provided value.
    """
    def assertion(actual):
        assert actual == expected, f"Expected {actual} to equal {expected}"
    return assertion


def not_equal_to(expected):
    """
    Asserts that the actual value is not equal to the provided value.

    Args:
        expected: The value to check for inequality against the actual value.

    Examples:
        >>> from reqflow import Client, given
        >>> from reqflow.assertions import not_equal_to
        >>> client = Client(base_url="https://httpbin.org")
        >>> given(client).when("GET", "/get?foo=bar").then().assert_body("url", not_equal_to("https://httpbin.org/get?foo=bar"))

    Returns:
        An assertion function that checks if the actual value is not equal to the provided value.
    """
    def assertion(actual):
        assert actual != expected, f"Expected {actual} to not equal {expected}"
    return assertion


def greater_than(expected):
    """
    Asserts that the actual value is greater than the provided value.

    Args:
        expected: The value to check for greater than the actual value.

    Examples:
        >>> from reqflow import Client, given
        >>> from reqflow.assertions import greater_than
        >>> client = Client(base_url="https://httpbin.org")
        >>> given(client).when("GET").then().assert_body("some_value", greater_than("777"))


    Returns:
        An assertion function that checks if the actual value is greater than the provided value.
    """
    def assertion(actual):
        assert actual > expected, f"Expected {actual} to be greater than {expected}"
    return assertion


def less_than(expected):
    """
    Asserts that the actual value is less than the provided value.

    Args:
        expected: The value to check for less than the actual value.

    Examples:
        >>> from reqflow import Client, given
        >>> from reqflow.assertions import greater_than
        >>> client = Client(base_url="https://httpbin.org")
        >>> given(client).when("GET").then().assert_body("some_value", less_than("777"))

    Returns:
        An assertion function that checks if the actual value is less than the provided value.

    """
    def assertion(actual):
        assert actual < expected, f"Expected {actual} to be less than {expected}"
    return assertion


def list_contains(expected):
    """
    Asserts that the actual value is contained in the response array list.

    Args:
        expected: The list to check for the actual value.

    Examples:
        >>> from reqflow import Client, given
        >>> from reqflow.assertions import list_contains
        >>> client = Client(base_url="https://httpbin.org")
        >>> given(client).when("GET").then().assert_body("json.some_array", list_contains(["foo", "bar", "baz"]))

    Returns:
        An assertion function that checks if the actual value is contained in the provided list.
    """
    def assertion(actual):
        assert expected in actual, f"Expected list {actual} to contain {expected}"
    return assertion


def is_none():
    """
    Asserts that the actual value is None.

    Examples:
        >>> from reqflow import Client, given
        >>> from reqflow.assertions import is_none
        >>> client = Client(base_url="https://httpbin.org")
        >>> given(client).when("GET").then().assert_body("json.some_value", is_none())

    Returns:
        An assertion function that checks if the actual value is None.
    """
    def assertion(actual):
        assert actual is None, f"Expected {actual} to be None"
    return assertion


def is_not_none():
    """
    Asserts that the actual value is not None.

    Examples:
        >>> from reqflow import Client, given
        >>> from reqflow.assertions import is_none
        >>> client = Client(base_url="https://httpbin.org")
        >>> given(client).when("GET").then().assert_body("json.some_value", is_not_none())

    Returns:
        An assertion function that checks if the actual value is not None.
    """
    def assertion(actual):
        assert actual is not None, f"Expected {actual} to not be None"
    return assertion


def matches_regex(pattern):
    """
    Asserts that the actual value matches the provided regex pattern.

    Args:
        pattern: A regex pattern to match against the actual value.

    Examples:
        >>> from reqflow import Client, given
        >>> from reqflow.assertions import matches_regex
        >>> client = Client(base_url="https://httpbin.org")
        >>> given(client).when("GET").then().assert_body("json.some_value", matches_regex(r"^\d{3}$"))

    Returns:
        An assertion function that checks if the actual value matches the provided regex pattern.

    """
    def assertion(actual):
        assert re.match(pattern, actual), f"Expected {actual} to match regex pattern {pattern}"
    return assertion


def and_(*assertions):
    """
    Combines multiple assertions with a logical AND, requiring all assertions to pass.

    Args:
        *assertions: A variable number of assertion functions.

    Examples:
        >>> from reqflow import Client, given
        >>> from reqflow.assertions import and_, greater_than, less_than
        >>> client = Client(base_url="https://httpbin.org")
        >>> given(client).when("GET").then().assert_body("json.some_value", and_(greater_than(1), less_than(100)))

    Returns:
        A combined assertion function that checks all provided assertions.
    """
    def combined_assertion(actual):
        for assertion in assertions:
            assertion(actual)
    return combined_assertion


def or_(*assertions):
    """
    Combines multiple assertions with a logical OR, requiring at least one assertion to pass.

    Args:
        *assertions: A variable number of assertion functions.

    Examples:
        >>> from reqflow import Client, given
        >>> from reqflow.assertions import or_, greater_than, less_than
        >>> client = Client(base_url="https://httpbin.org")
        >>> given(client).when("GET").then().assert_body("json.some_value", or_(greater_than(1), less_than(100)))

    Returns:
        A combined assertion function that checks if any of the provided assertions pass.
    """
    def combined_assertion(actual):
        errors = []
        for assertion in assertions:
            try:
                assertion(actual)
                return
            except AssertionError as e:
                errors.append(str(e))
        raise AssertionError(" OR ".join(errors))
    return combined_assertion
