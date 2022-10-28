from ninja import NinjaAPI
from ninja.errors import AuthenticationError
from ninja.responses import Response

from api.internal.v1.competencies.api import register_competencies_api
from api.internal.v1.departments.api import register_departments_api
from api.internal.v1.exceptions import BadRequestError, NotFoundError, UnauthorizedError
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


def get_api() -> NinjaAPI:
    base = NinjaAPI(title="HR")

    add_exceptions(base)

    for register in apis_registrations:
        register(base)

    return base


def add_exceptions(base: NinjaAPI) -> None:
    base.add_exception_handler(BadRequestError, lambda r, exc: Response(MessageResponse(msg=exc.msg), status=400))
    base.add_exception_handler(
        AuthenticationError, lambda r, exc: Response(MessageResponse(msg="Unauthorized"), status=401)
    )
    base.add_exception_handler(UnauthorizedError, lambda r, exc: Response(MessageResponse(msg=exc.msg), status=401))
    base.add_exception_handler(NotFoundError, lambda r, exc: Response(MessageResponse(msg=exc.msg), status=404))
