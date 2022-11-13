from api.internal.v1.errors import DomainErrorBase


class YouCannotAddUnpublishedVacancyToWishlistError(DomainErrorBase):
    @property
    def code(self) -> int:
        return 2

    @property
    def msg(self) -> str:
        return "You cannot add an unpublished vacancy to wishlist"


class VacancyAlreadyAddedToWishlistError(DomainErrorBase):
    @property
    def code(self) -> int:
        return 3

    @property
    def msg(self) -> str:
        return "The vacancy already added to wishlist"
