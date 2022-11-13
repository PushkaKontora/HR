from django.conf import settings

from api.internal.errors import DomainErrorBase


class ResumeIsNotPDFError(DomainErrorBase):
    @property
    def code(self) -> int:
        return 1

    @property
    def msg(self) -> str:
        return "The resume file is not pdf"


class ResumeIsLargeError(DomainErrorBase):
    @property
    def code(self) -> int:
        return 2

    @property
    def msg(self) -> str:
        return f"Size of resume file must be lte than {settings.MAX_FILE_SIZE_BYTES} bytes"
