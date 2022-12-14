from typing import List, Union

from django.db.models import QuerySet

from api.models import Vacancy
from tests.v1.integrations.conftest import V1, datetime_to_string

VACANCIES = V1 + "/vacancies"
VACANCY = VACANCIES + "/{vacancy_id}"


def vacancy_out(vacancy: Vacancy) -> dict:
    department = vacancy.department
    leader = department.leader

    return {
        "id": vacancy.id,
        "name": vacancy.name,
        "description": vacancy.description,
        "expected_experience": str(vacancy.expected_experience),
        "salary_from": vacancy.salary_from,
        "salary_to": vacancy.salary_to,
        "department": {
            "id": department.id,
            "name": department.name,
            "description": department.description,
            "leader": {
                "id": leader.id,
                "surname": leader.surname,
                "name": leader.name,
                "patronymic": leader.patronymic,
            },
        },
        "published_at": datetime_to_string(vacancy.published_at) if vacancy.published_at else None,
    }


def vacancies_out(vacancies: Union[QuerySet[Vacancy], List[Vacancy]]) -> dict:
    return {
        "items": [vacancy_out(vacancy) for vacancy in vacancies],
        "count": vacancies.count() if vacancies is QuerySet else len(vacancies),
    }
