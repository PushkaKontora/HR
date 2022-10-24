from ninja import NinjaAPI

from api.internal.v1.competencies.api import register_competencies_api
from api.internal.v1.departments.api import register_departments_api
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

    for register in apis_registrations:
        register(base)

    return base
