from api.internal.v1.errors import APIBaseError


class ResumeIsNotPDFError(APIBaseError):
    def __init__(self):
        super(ResumeIsNotPDFError, self).__init__(1, "The resume file is not pdf", 422)
