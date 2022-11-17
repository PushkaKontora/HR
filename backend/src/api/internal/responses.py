from ninja import Schema


class MessageResponse(Schema):
    msg: str

    @staticmethod
    def create(msg: str) -> "MessageResponse":
        return MessageResponse(msg=msg)


class SuccessResponse(MessageResponse):
    msg = "Success"


class DomainErrorDetails(Schema):
    code: int
    msg: str


class DomainErrorResponse(Schema):
    error: DomainErrorDetails
