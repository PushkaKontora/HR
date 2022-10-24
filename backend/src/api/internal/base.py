from ninja import Schema

NOT_READY_TAG = "not ready"


class SuccessResponse(Schema):
    pass


class ErrorDetails(Schema):
    code: int
    message: str


class ErrorResponse(Schema):
    error: ErrorDetails
