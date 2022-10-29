from typing import Any, Optional

from django.http import HttpRequest
from ninja.security import HttpBearer

from api.internal.v1.exceptions import UnauthorizedError
from api.internal.v1.users.domain.entities import TokenType
from api.internal.v1.users.presentation.handlers import IJWTService


class JWTAuth(HttpBearer):
    TOKEN_IS_EXPIRED = "The token is expired"
    UNKNOWN_USER_ID = "Unknown user id"
    INVALID_SIGNATURE_OR_PAYLOAD = "Invalid signature or payload"

    def __init__(self, jwt_service: IJWTService):
        super(JWTAuth, self).__init__()

        self.service = jwt_service

    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        request.user = None

        payload = self.service.try_get_payload(token)
        if not payload or not self.service.is_type(payload, TokenType.ACCESS):
            raise UnauthorizedError(self.INVALID_SIGNATURE_OR_PAYLOAD)

        if self.service.is_token_expired(payload):
            raise UnauthorizedError(self.TOKEN_IS_EXPIRED)

        user = self.service.try_get_user(payload)
        if not user:
            raise UnauthorizedError(self.UNKNOWN_USER_ID)

        request.user = user

        return token
