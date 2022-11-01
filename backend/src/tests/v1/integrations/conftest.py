from datetime import datetime
from typing import Optional

from django.test import Client
from ninja.responses import Response

V1 = "/v1"

CONTENT_TYPE = "application/json"
AUTHORIZATION_HEADER = "HTTP_AUTHORIZATION"


def get_headers(token: Optional[str]) -> dict:
    return {AUTHORIZATION_HEADER: f"Bearer {token}"} if token is not None else {}


def get(client: Client, uri: str, token: str = None) -> Response:
    return client.get(uri, content_type=CONTENT_TYPE, **get_headers(token))


def post(client: Client, uri: str, token: str = None, body: dict = None) -> Response:
    return client.post(uri, body, content_type=CONTENT_TYPE, **get_headers(token))


def put(client: Client, uri: str, token: str = None, body: dict = None) -> Response:
    return client.put(uri, body, content_type=CONTENT_TYPE, **get_headers(token))


def patch(client: Client, uri: str, token: str = None, body: dict = None) -> Response:
    return client.patch(uri, body, content_type=CONTENT_TYPE, **get_headers(token))


def delete(client: Client, uri: str, token: str = None) -> Response:
    return client.delete(uri, content_type=CONTENT_TYPE, **get_headers(token))


def error_422(code: int, message: str) -> dict:
    return {"error": {"code": code, "msg": message}}


def success() -> dict:
    return message("Success")


def unauthorized() -> dict:
    return message("Unauthorized")


def forbidden(msg: str = "Forbidden") -> dict:
    return message(msg)


def not_found(resource: str = None) -> dict:
    return message("Not found" + (f" {resource}" if resource else ""))


def message(msg: str) -> dict:
    return {"msg": msg}


def datetime_to_string(time: datetime) -> str:
    string = time.strftime("%Y-%m-%dT%H:%M:%S")

    if time.microsecond > 0:
        string += f".{str(time.microsecond // 1000).zfill(3)}Z"
    else:
        string += "Z"

    return string
