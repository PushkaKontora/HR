from api.internal.v1.exceptions import APIBaseError


class ResumeIsCreatedByUserError(APIBaseError):
    def __init__(self):
        super(ResumeIsCreatedByUserError, self).__init__(1, "The user has already created a resume", 422)


class AttachedDocumentIsNotPDFError(APIBaseError):
    def __init__(self):
        super(AttachedDocumentIsNotPDFError, self).__init__(2, "The attached document is not a pdf file", 422)


class ResumeAlreadyAddedToWishlistError(APIBaseError):
    def __init__(self):
        super(ResumeAlreadyAddedToWishlistError, self).__init__(3, "The resume already added to wishlist", 422)


class UnpublishedResumeCannotBeAddedToWishlistError(APIBaseError):
    def __init__(self):
        super(UnpublishedResumeCannotBeAddedToWishlistError, self).__init__(
            4, "You cannot add a unpublished resume to wishlist", 422
        )
