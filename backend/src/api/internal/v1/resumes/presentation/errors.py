from django.conf import settings

from api.internal.v1.errors import DomainErrorBase


class ResumeIsCreatedByUserError(DomainErrorBase):
    @property
    def code(self) -> int:
        return 1

    @property
    def msg(self) -> str:
        return "The user has already created a resume"


class AttachedDocumentIsNotPDFError(DomainErrorBase):
    @property
    def code(self) -> int:
        return 2

    @property
    def msg(self) -> str:
        return "The attached document is not a pdf file"


class ResumeAlreadyAddedToWishlistError(DomainErrorBase):
    @property
    def code(self) -> int:
        return 3

    @property
    def msg(self) -> str:
        return "The resume already added to wishlist"


class UnpublishedResumeCannotBeAddedToWishlistError(DomainErrorBase):
    @property
    def code(self) -> int:
        return 4

    @property
    def msg(self) -> str:
        return "You cannot add an unpublished resume to wishlist"


class AttachedDocumentIsLargeSizeError(DomainErrorBase):
    @property
    def code(self) -> int:
        return 5

    @property
    def msg(self) -> str:
        return f"The attached document size must be lte than {settings.MAX_FILE_SIZE_BYTES} bytes"
