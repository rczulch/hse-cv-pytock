#
# exceptions.py
#

class CustomError(Exception):
    """Base exception for application-specific errors."""
    pass

class InvalidInputError(CustomError):
    """Raised when input data is invalid."""
    pass

class InternalError(CustomError):
    """Raised on failures due to other than user activity."""
    pass

class DuplicateNameError(CustomError):
    """Raised when creating a named resource that already exists."""
    pass

class TableBusyError(CustomError):
    """Raised when booking a table that is already busy."""
    pass

class TableFreeError(CustomError):
    """Raised when releasing a table that was already free."""
    pass

class DuplicateBookingError(CustomError):
    """Raised when booking a table that conflicts with another by the same name/phone."""
    pass