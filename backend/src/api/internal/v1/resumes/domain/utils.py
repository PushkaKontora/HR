import uuid

from ninja import UploadedFile


def get_resume_filename(document: UploadedFile) -> str:
    return f"{uuid.uuid4().hex}_{document.name.replace(' ', '-').replace('_', '-')}"
