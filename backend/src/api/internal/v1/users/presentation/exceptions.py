from api.internal.v1.exceptions import APIBaseException


class PasswordHasAlreadyRegistered(APIBaseException):
    def __init__(self):
        super(PasswordHasAlreadyRegistered, self).__init__(1, "The email has already registered", 422)


class PasswordDoesNotMatch(APIBaseException):
    def __init__(self):
        super(PasswordDoesNotMatch, self).__init__(2, "The previous password does not match with expected", 422)
