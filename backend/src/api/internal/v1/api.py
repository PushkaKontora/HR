from ninja import NinjaAPI

from api.internal.errors import add_common_errors_to_api
from api.internal.v1.competencies.api import register_competencies_api
from api.internal.v1.departments.api import register_departments_api
from api.internal.v1.resumes.api import register_resumes_api
from api.internal.v1.users.api import register_users_api
from api.internal.v1.vacancies.api import register_vacancies_api
from api.internal.v1.vacancy_requests.api import register_vacancy_requests_api

apis = [
    register_users_api,
    register_departments_api,
    register_resumes_api,
    register_vacancies_api,
    register_competencies_api,
    register_vacancy_requests_api,
]


def get_v1_api() -> NinjaAPI:
    base = NinjaAPI(title="HR")

    add_common_errors_to_api(base)

    for register in apis:
        register(base)

    return base
