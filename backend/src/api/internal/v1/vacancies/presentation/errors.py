from api.internal.v1.errors import APIBaseError


class UnknownDepartmentIdError(APIBaseError):
    def __init__(self):
        super(UnknownDepartmentIdError, self).__init__(1, "Unknown department_id", 422)


class YouCannotAddUnpublishedVacancyToWishlistError(APIBaseError):
    def __init__(self):
        super(YouCannotAddUnpublishedVacancyToWishlistError, self).__init__(
            2, "You cannot add an unpublished vacancy to wishlist", 422
        )


class VacancyAlreadyAddedToWishlistError(APIBaseError):
    def __init__(self):
        super(VacancyAlreadyAddedToWishlistError, self).__init__(3, "The vacancy already added to wishlist", 422)


class ResumeIsNotPDFError(APIBaseError):
    def __init__(self):
        super(ResumeIsNotPDFError, self).__init__(4, "The resume file is not pdf", 422)
