import uuid

from bcrypt import hashpw
from django.conf import settings
from ninja import UploadedFile


def hash_password(password: str) -> str:
    return hashpw(password.encode("utf-8"), settings.SALT).decode()


def get_photo_filename(photo: UploadedFile) -> str:
    return f"{uuid.uuid4().hex}_{photo.name.replace(' ', '-').replace('_', '-')}"
