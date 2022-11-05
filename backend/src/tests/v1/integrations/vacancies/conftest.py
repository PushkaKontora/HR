import pytest

from api.models import Department, Permission, User
from tests.v1.integrations.conftest import V1

VACANCIES = V1 + "/vacancies"
VACANCY = VACANCIES + "/{vacancy_id}"


@pytest.fixture
def department(employer: User) -> Department:
    return Department.objects.create(leader=employer, name="123")


@pytest.fixture
def another_employer(email="asadfsdfsd@gmail.com", surname="Pupkin", name="Denis", patronymic="Dykovich") -> User:
    return User.objects.create(
        email=email, surname=surname, name=name, patronymic=patronymic, permission=Permission.EMPLOYER
    )
