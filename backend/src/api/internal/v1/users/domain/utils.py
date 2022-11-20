from bcrypt import hashpw
from django.conf import settings
from ninja import UploadedFile


def hash_password(password: str) -> str:
    return hashpw(password.encode("utf-8"), settings.SALT).decode()


def get_photo_filename(photo: UploadedFile, user_id: int) -> str:
    extension = photo.name.split(".")[1]
    return f"photo_{user_id}.{extension}"
