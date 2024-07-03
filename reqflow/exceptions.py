class GivenInitializationError(Exception):
    """Raised when the parameters of the `given` function are passed incorrectly."""
    def __init__(self, message, parameters):
        super().__init__(message)
        self.parameters = parameters

class InvalidArgumentError(Exception):
    """Raised when an argument to a function is not of the expected type or format."""
    pass

class InvalidCredentialsError(Exception):
    """Raised when the credentials provided for authentication are not valid."""
    pass

class ValidationError(Exception):
    """Raised when the data does not match the expected format"""
    pass