class AppError(Exception):
    """Base class for every error this service raises on purpose."""


class NotFoundError(AppError):
    """A requested resource does not exist."""


class InvalidInputError(AppError):
    """Input breaks a business rule."""
