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


def get_422_error(code: int, message: str) -> dict:
    return {"error": {"code": code, "msg": message}}
