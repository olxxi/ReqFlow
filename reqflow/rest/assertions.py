def is_(expected):
    def assertion(actual):
        assert actual == expected, f"Expected {actual} to be {expected}"
    return assertion


def contains_string(expected):
    def assertion(actual):
        assert expected in actual, f"Expected '{actual}' to contain string '{expected}'"
    return assertion


def equal_to(expected):
    def assertion(actual):
        assert actual == expected, f"Expected {actual} to equal {expected}"
    return assertion
