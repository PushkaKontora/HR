from itertools import chain

from ninja import Schema

NOT_READY_TAG = "not ready"


def to_camel_case(string: str) -> str:
    head, *tail = string.split("_")

    return "".join(chain(head, *map(str.title, tail)))


class BaseSchema(Schema):
    class Config:
        alias_generator = to_camel_case
        allow_population_by_field_name = True


class SuccessResponse(BaseSchema):
    pass


class ErrorDetails(BaseSchema):
    code: int
    message: str


class ErrorResponse(BaseSchema):
    error: ErrorDetails
