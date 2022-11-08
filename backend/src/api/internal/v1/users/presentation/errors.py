from api.internal.v1.errors import APIBaseError


class PasswordHasAlreadyRegisteredError(APIBaseError):
    def __init__(self):
        super(PasswordHasAlreadyRegisteredError, self).__init__(1, "The email has already registered", 422)


class PasswordDoesNotMatchError(APIBaseError):
    def __init__(self):
        super(PasswordDoesNotMatchError, self).__init__(2, "The previous password does not match with expected", 422)


class UserIsLeaderOfDepartmentError(APIBaseError):
    def __init__(self):
        super(UserIsLeaderOfDepartmentError, self).__init__(10, "The user is a leader of a department", 422)


class EmailIsAlreadyRegisteredError(APIBaseError):
    def __init__(self):
        super(EmailIsAlreadyRegisteredError, self).__init__(11, "The email is already registered", 422)


class FileIsNotImageError(APIBaseError):
    def __init__(self):
        super(FileIsNotImageError, self).__init__(12, "The file is not image", 422)
