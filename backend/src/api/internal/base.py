from abc import ABC

from ninja import Schema
from ninja.responses import Response

NOT_IMPLEMENTED_TAG = "not implemented"


class SuccessResponse(Schema):
    msg: str = "Success"


class ErrorDetails(Schema):
    code: int
    msg: str


class ErrorResponse(Schema):
    error: ErrorDetails


class APIBaseException(Exception, ABC):
    def __init__(self, code: int, msg: str, status: int):
        self.status = status
        self.code = code
        self.msg = msg

    @classmethod
    def response(cls, exc: "APIBaseException") -> Response:
        return Response(ErrorResponse(error=ErrorDetails(code=exc.code, msg=exc.msg)), status=exc.status)
