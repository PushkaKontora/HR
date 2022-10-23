from abc import ABC, abstractmethod
from typing import Any, Optional

from django.http import HttpRequest
from ninja.security import HttpBearer

from api.internal.models import User


class JWTBaseAuthentication(HttpBearer, ABC):
    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        pass

    @abstractmethod
    def authorize(self, user: User) -> bool:
        pass


class JWTAuthenticationStub(JWTBaseAuthentication):
    def authorize(self, user: User) -> bool:
        pass
