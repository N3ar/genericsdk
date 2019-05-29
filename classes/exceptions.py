class GenericError(Exception):
    def __init__(self, message=None, errors=None):
        if errors:
            message = ', '.join(errors)

        self.errors = errors

        super(GenericError, self).__init__(message)


class InvalidRequest(GenericError):
    pass


class Unauthorized(GenericError):
    pass


class Forbidden(GenericError):
    pass


class InvalidPath(GenericError):
    pass


class RateLimitExceeded(GenericError):
    pass


class InternalServerError(GenericError):
    pass


class UnexpectedError(GenericError):
    pass
