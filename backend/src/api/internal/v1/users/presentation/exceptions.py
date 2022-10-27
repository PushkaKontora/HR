from api.internal.base import APIBaseException


class PasswordHasAlreadyRegistered(APIBaseException):
    def __init__(self):
        super(PasswordHasAlreadyRegistered, self).__init__(1, "The email has already registered", 422)
