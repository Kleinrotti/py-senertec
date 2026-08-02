class SenertecError(Exception):
    """Raised on errors with senertec platform."""


class LoginError(SenertecError):
    """Base error for login failures."""


class InvalidCredentialsError(LoginError):
    """Username or password rejected by the SSO server."""


class LoginServerError(LoginError):
    """Login server was unreachable or returned an error status."""