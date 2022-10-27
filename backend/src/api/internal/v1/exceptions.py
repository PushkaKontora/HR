from abc import ABC

from ninja.responses import Response

from api.internal.v1.responses import ErrorDetails, ErrorResponse


class APIBaseException(Exception, ABC):
    def __init__(self, code: int, msg: str, status: int):
        self.status = status
        self.code = code
        self.msg = msg

    @classmethod
    def response(cls, exc: "APIBaseException") -> Response:
        return Response(ErrorResponse(error=ErrorDetails(code=exc.code, msg=exc.msg)), status=exc.status)


class Unauthorized(Exception):
    pass
