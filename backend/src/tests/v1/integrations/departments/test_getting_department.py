import pytest
from django.test import Client
from ninja.responses import Response

from api.models import Department, Vacancy
from tests.v1.integrations.conftest import get, not_found
from tests.v1.integrations.departments.conftest import DEPARTMENT


def get_one(client: Client, department_id: int) -> Response:
    return get(client, DEPARTMENT.format(department_id=department_id))


def department_out(department: Department, vacancies_amount: int) -> dict:
    leader = department.leader

    return {
        "id": department.id,
        "name": department.name,
        "description": department.description,
        "vacancies_amount": vacancies_amount,
        "leader": {
            "id": leader.id,
            "surname": leader.surname,
            "name": leader.name,
            "patronymic": leader.patronymic,
        },
    }


@pytest.mark.integration
@pytest.mark.django_db
def test_get_one(client: Client, department: Department, vacancies_amount=3) -> None:
    Vacancy.objects.bulk_create(Vacancy(department=department, name="456") for _ in range(vacancies_amount))

    response = get_one(client, department.id)

    assert response.status_code == 200
    assert response.json() == department_out(department, vacancies_amount)


@pytest.mark.integration
@pytest.mark.django_db
def test_get_one__unknown_id(client: Client, department: Department) -> None:
    response = get_one(client, 0)

    assert response.status_code == 404
    assert response.json() == not_found()
