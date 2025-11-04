#
# exceptions.py
#

class CustomError(Exception):
    """Base exception for application-specific errors."""
    pass

class InvalidInputError(CustomError):
    """Raised when input data is invalid."""
    pass

class DuplicateNameError(CustomError):
    """Raised when creating a named resource that already exists."""
    pass