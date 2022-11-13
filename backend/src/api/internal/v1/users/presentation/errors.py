from api.internal.v1.errors import DomainErrorBase


class EmailHasAlreadyRegisteredError(DomainErrorBase):
    @property
    def code(self) -> int:
        return 1

    @property
    def msg(self) -> str:
        return "The email has already registered"


class PasswordDoesNotMatchError(DomainErrorBase):
    @property
    def code(self) -> int:
        return 2

    @property
    def msg(self) -> str:
        return "The previous password does not match with expected"


class UserIsLeaderOfDepartmentError(DomainErrorBase):
    @property
    def code(self) -> int:
        return 10

    @property
    def msg(self) -> str:
        return "The user is a leader of a department"


class EmailIsAlreadyRegisteredError(DomainErrorBase):
    @property
    def code(self) -> int:
        return 11

    @property
    def msg(self) -> str:
        return "The email is already registered"


class FileIsNotImageError(DomainErrorBase):
    @property
    def code(self) -> int:
        return 12

    @property
    def msg(self) -> str:
        return "The file is not an image"
