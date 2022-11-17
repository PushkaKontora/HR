from abc import ABC, abstractmethod
from typing import Iterable, Type

from ninja import NinjaAPI
from ninja.errors import AuthenticationError
from ninja.responses import Response

from api.internal.responses import DomainErrorDetails, DomainErrorResponse, MessageResponse


class APIErrorBase(Exception, ABC):
    pass


class DomainErrorBase(APIErrorBase, ABC):
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
        return Response(DomainErrorResponse(error=DomainErrorDetails(code=exc.code, msg=exc.msg)), status=422)


class UnauthorizedError(APIErrorBase):
    def __init__(self, msg: str = "Unauthorized"):
        self.msg = msg


class NotFoundError(APIErrorBase):
    def __init__(self, resource: str = None):
        self.msg = "Not found" + (f" {resource}" if resource else "")


class BadRequestError(APIErrorBase):
    def __init__(self, msg: str = None):
        self.msg = msg or "Bad request"


class ForbiddenError(APIErrorBase):
    def __init__(self, msg: str = "Forbidden"):
        self.msg = msg


def add_common_errors_to_api(base: NinjaAPI) -> None:
    base.add_exception_handler(BadRequestError, lambda r, exc: Response(MessageResponse(msg=exc.msg), status=400))
    base.add_exception_handler(
        AuthenticationError, lambda r, exc: Response(MessageResponse(msg="Unauthorized"), status=401)
    )
    base.add_exception_handler(UnauthorizedError, lambda r, exc: Response(MessageResponse(msg=exc.msg), status=401))
    base.add_exception_handler(ForbiddenError, lambda r, exc: Response(MessageResponse(msg=exc.msg), status=403))
    base.add_exception_handler(NotFoundError, lambda r, exc: Response(MessageResponse(msg=exc.msg), status=404))


def add_domain_errors_to_api(api: NinjaAPI, errors: Iterable[Type[DomainErrorBase]]) -> None:
    for exception_cls in errors:
        api.add_exception_handler(exception_cls, _get_handler(exception_cls))


def _get_handler(exception_cls: Type[DomainErrorBase]):
    return lambda request, exc: exception_cls.response(exc)
