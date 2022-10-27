from ninja import Schema


class MessageResponse(Schema):
    msg: str


class SuccessResponse(MessageResponse):
    msg: str = "Success"


class ErrorDetails(Schema):
    code: int
    msg: str


class ErrorResponse(Schema):
    error: ErrorDetails
