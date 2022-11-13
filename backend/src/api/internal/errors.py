from abc import ABC, abstractmethod

from ninja.responses import Response

from api.internal.responses import ErrorDetails, ErrorResponse


class DomainErrorBase(Exception, ABC):
    @property
    @abstractmethod
    def code(self) -> int:
        pass

    @property
    @abstractmethod
    def msg(self) -> str:
        pass

    @classmethod
    def response(cls, exc: "DomainErrorBase") -> Response:
        return Response(ErrorResponse(error=ErrorDetails(code=exc.code, msg=exc.msg)), status=422)


class UnauthorizedError(Exception):
    def __init__(self, msg: str = "Unauthorized"):
        self.msg = msg


class NotFoundError(Exception):
    def __init__(self, resource: str = None):
        self.msg = "Not found" + (f" {resource}" if resource else "")


class BadRequestError(Exception):
    def __init__(self, msg: str = None):
        self.msg = msg or "Bad request"


class ForbiddenError(Exception):
    def __init__(self, msg: str = "Forbidden"):
        self.msg = msg
