class AppError(Exception):
    """Base class for every error this worker raises on purpose."""


class InvalidInputError(AppError):
    """Input breaks a business rule."""


class ServiceUnavailableError(AppError):
    """A system this worker depends on cannot answer right now."""
