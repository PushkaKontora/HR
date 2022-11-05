from api.internal.v1.exceptions import APIBaseError


class UnknownDepartmentIdError(APIBaseError):
    def __init__(self):
        super(UnknownDepartmentIdError, self).__init__(1, "Unknown department_id", 422)
