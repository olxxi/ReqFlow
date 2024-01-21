import re


def contains_string(expected):
    """
    Asserts that the actual value contains the provided string.
    Args:
        expected: The string to check for in the actual value.

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

    Returns:
        An assertion function that checks if the actual value is less than the provided value.

    """
    def assertion(actual):
        assert actual < expected, f"Expected {actual} to be less than {expected}"
    return assertion


def contains_in_list(expected):
    """
    Asserts that the actual value is contained in the provided list.
    Args:
        expected: The list to check for the actual value.

    Returns:
        An assertion function that checks if the actual value is contained in the provided list.
    """
    def assertion(actual):
        assert expected in actual, f"Expected list {actual} to contain {expected}"
    return assertion


def is_none():
    """
    Asserts that the actual value is None.
    Returns:
        An assertion function that checks if the actual value is None.
    """
    def assertion(actual):
        assert actual is None, f"Expected {actual} to be None"
    return assertion


def is_not_none():
    """
    Asserts that the actual value is not None.
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
