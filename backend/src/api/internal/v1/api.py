from ninja import NinjaAPI
from ninja.errors import AuthenticationError
from ninja.responses import Response

from api.internal.v1.competencies.api import register_competencies_api
from api.internal.v1.departments.api import register_departments_api
from api.internal.v1.exceptions import Unauthorized
from api.internal.v1.responses import MessageResponse
from api.internal.v1.resumes.api import register_resumes_api
from api.internal.v1.users.api import register_users_api
from api.internal.v1.vacancies.api import register_vacancies_api

apis_registrations = [
    register_users_api,
    register_departments_api,
    register_resumes_api,
    register_vacancies_api,
    register_competencies_api,
]

UNAUTHORIZED_RESPONSE = Response(MessageResponse(msg="Unauthorized"), status=401)


def get_api() -> NinjaAPI:
    base = NinjaAPI(title="HR")

    base.add_exception_handler(Unauthorized, lambda resp, exc: UNAUTHORIZED_RESPONSE)
    base.add_exception_handler(AuthenticationError, lambda resp, exc: UNAUTHORIZED_RESPONSE)

    for register in apis_registrations:
        register(base)

    return base
