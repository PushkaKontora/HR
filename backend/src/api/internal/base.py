from ninja import Schema

NOT_IMPLEMENTED_TAG = "not implemented"


class SuccessResponse(Schema):
    pass


class ErrorDetails(Schema):
    code: int
    message: str


class ErrorResponse(Schema):
    error: ErrorDetails
