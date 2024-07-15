class ProjectApiError(Exception):
    """base exception class"""

    def __init__(self, message: str = "Service is unavailable", name: str = "SkyPulse"):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)


class ServiceError(ProjectApiError):
    """failures in external services or APIs, like a database or a third-party service"""

    pass


class TypingError(ProjectApiError):
    """invalid typing input"""

    pass


class AuthenticationFailed(ProjectApiError):
    """unexpected error"""

    pass
