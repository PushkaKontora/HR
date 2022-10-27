from datetime import timedelta

from django.conf import settings
from django.utils.timezone import now

from api.models import User
from tests.conftest import V1

USERS = V1 + "/users"


def access_payload(user: User) -> dict:
    return payload(user, "access", settings.ACCESS_TOKEN_TTL)


def refresh_payload(user: User) -> dict:
    return payload(user, "refresh", settings.REFRESH_TOKEN_TTL)


def payload(user: User, token_type: str, ttl: timedelta) -> dict:
    return {
        "type": token_type,
        "user_id": user.id,
        "permission": str(user.permission),
        "exp": int((now() + ttl).timestamp()),
    }
