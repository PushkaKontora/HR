from api.internal.v1.errors import DomainErrorBase


class ResumeIsNotPDFError(DomainErrorBase):
    @property
    def code(self) -> int:
        return 1

    @property
    def msg(self) -> str:
        return "The resume file is not pdf"
