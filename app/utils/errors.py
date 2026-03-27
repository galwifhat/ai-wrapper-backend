class AIServiceError(Exception):
    """Raised when OpenRouter returns an error."""

    pass


class ValidationError(Exception):
    """Raised on bad request data."""

    pass
