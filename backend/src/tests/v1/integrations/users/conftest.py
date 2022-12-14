from datetime import timedelta

import pytest
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import now
from jwt import decode, encode
from ninja import UploadedFile

from api.models import User
from tests.v1.integrations.conftest import V1

USERS = V1 + "/users"
USER = USERS + "/{user_id}"


def access_payload(user: User) -> dict:
    return payload(user, "access", settings.ACCESS_TOKEN_TTL)


def refresh_payload(user: User) -> dict:
    return payload(user, "refresh", settings.REFRESH_TOKEN_TTL)


def payload(user: User, token_type: str, ttl: timedelta) -> dict:
    return {
        "type": token_type,
        "user_id": user.id,
        "permission": str(user.permission),
        "expires_in": int((now() + ttl).timestamp()),
    }


def encode_payload(_payload: dict) -> str:
    return encode(_payload, settings.SECRET_KEY)


def decode_payload(token: str) -> dict:
    return decode(token, settings.SECRET_KEY, "HS256")
