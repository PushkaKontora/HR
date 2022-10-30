import random

import pytest
from django.test import Client
from ninja.responses import Response

from api.models import Department, User
from tests.v1.integrations.conftest import get
from tests.v1.integrations.departments.conftest import DEPARTMENTS
from tests.v1.integrations.departments.test_getting_department import department_out


def get_many(client: Client) -> Response:
    return get(client, DEPARTMENTS)


@pytest.mark.integration
@pytest.mark.django_db
def test_get_all(client: Client, departments_amount=3) -> None:
    users = User.objects.bulk_create(
        User(email=f"{i}@gmail.com", surname="1", name="2", patronymic="3") for i in range(departments_amount)
    )
    departments = Department.objects.bulk_create(Department(leader=usr, name="1") for usr in users)

    response = get_many(client)

    assert response.status_code == 200
    assert response.json() == [department_out(department, 0) for department in departments]


@pytest.mark.integration
@pytest.mark.django_db
def test_get_all__empty_list(client: Client) -> None:
    response = get_many(client)

    assert response.status_code == 200
    assert response.json() == []
