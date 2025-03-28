class ToolError(Exception):
    """Raised when a tool encounters an error."""

    def __init__(self, message):
        self.message = message


class AutonomaError(Exception):
    """Base exception for all Autonoma errors"""
    pass


class TokenLimitExceeded(AutonomaError):
    """Exception raised when the token limit is exceeded"""
    pass
