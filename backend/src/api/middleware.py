from typing import Callable

from django.http import HttpRequest, HttpResponse
from ninja.responses import Response

from api.internal.responses import MessageResponse
from api.logging import get_logger


class Process500:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        return self.get_response(request)

    def process_exception(self, request: HttpRequest, exception: Exception) -> Response:
        get_logger(request).exception(exception)

        return Response(MessageResponse.create("Internal Server Error"), status=500)
