from logging import Handler, LogRecord
from typing import Callable
from uuid import uuid4

from django.http import HttpRequest, HttpResponse
from loguru import logger as logger_
from loguru._logger import Logger
from telegram import Bot


class RequestIdMiddleware:
    LENGTH = 10

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request.id = uuid4().hex[: self.LENGTH]

        return self.get_response(request)


class TelegramNotifier(Handler):
    def __init__(self, token: str, chat_id: int):
        super(TelegramNotifier, self).__init__()

        self._chat_id = chat_id
        self._bot = Bot(token)

    def emit(self, record: LogRecord) -> None:
        self._bot.send_document(
            chat_id=self._chat_id,
            document=self.get_content(record),
            filename=self.get_filename(record),
        )

    def get_content(self, record: LogRecord) -> bytes:
        return self.format(record).encode()

    def get_filename(self, record: LogRecord) -> str:
        return f"{record.exc_info[1]}.txt"


def get_logger(request: HttpRequest) -> "Logger":
    return logger_.bind(request_id=request.id)
