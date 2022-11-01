from api.internal.v1.exceptions import APIBaseError


class ResumeIsCreatedByUserError(APIBaseError):
    def __init__(self):
        super(ResumeIsCreatedByUserError, self).__init__(1, "The user has already created a resume", 422)


class AttachedDocumentIsNotPDFError(APIBaseError):
    def __init__(self):
        super(AttachedDocumentIsNotPDFError, self).__init__(2, "The attached document is not a pdf file", 422)
