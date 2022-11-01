from bcrypt import hashpw
from django.conf import settings


def hash_password(password: str) -> str:
    return hashpw(password.encode("utf-8"), settings.SALT).decode()
