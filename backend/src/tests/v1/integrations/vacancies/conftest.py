import pytest

from api.models import Department, Experience, Permission, User, Vacancy
from tests.v1.integrations.conftest import V1, datetime_to_string

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


@pytest.fixture
def vacancy(department: Department) -> Vacancy:
    return Vacancy.objects.create(
        department=department,
        name="New Vacancy",
        description="Big description",
        expected_experience=Experience.NO_EXPERIENCE,
    )


def vacancy_out(vacancy: Vacancy) -> dict:
    department = vacancy.department
    leader = department.leader

    return {
        "id": vacancy.id,
        "name": vacancy.name,
        "description": vacancy.description,
        "expected_experience": vacancy.expected_experience,
        "salary_from": vacancy.salary_from,
        "salary_to": vacancy.salary_to,
        "department": {
            "id": department.id,
            "name": department.name,
            "leader": {
                "id": leader.id,
                "surname": leader.surname,
                "name": leader.name,
                "patronymic": leader.patronymic,
            },
        },
        "published_at": datetime_to_string(vacancy.published_at) if vacancy.published_at else None,
    }
