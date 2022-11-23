import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from loguru import logger

from api.internal.v1.users.domain.utils import hash_password
from api.models import Department, Experience, Password, Permission, User, Vacancy
from tests.v1.integrations.users.conftest import access_payload, encode_payload

USER_PASSWORD = "13_очень secret password_37"
ANOTHER_USER_PASSWORD = "SeriousDim8"


@pytest.fixture
def user(email="address@gmail.com", surname="Sidorov", name="Ivan", patronymic="Fedorovich") -> User:
    return User.objects.create(
        email=email, surname=surname, name=name, patronymic=patronymic, permission=Permission.USER
    )


@pytest.fixture
def employer(email="address@mail.ru", surname="Perov", name="Dima", patronymic="Vladimirovich") -> User:
    return User.objects.create(
        email=email, surname=surname, name=name, patronymic=patronymic, permission=Permission.EMPLOYER
    )


@pytest.fixture
def another_user(email="a@gmail.com", surname="Lykov", name="Dima", patronymic="Unknown") -> User:
    return User.objects.create(email=email, surname=surname, name=name, patronymic=patronymic)


@pytest.fixture
def user_token(user: User) -> str:
    return encode_payload(access_payload(user))


@pytest.fixture
def employer_token(employer: User) -> str:
    return encode_payload(access_payload(employer))


@pytest.fixture
def user_with_password(user: User) -> User:
    Password.objects.create(owner=user, value=hash_password(USER_PASSWORD))

    return user


@pytest.fixture
def another_user_with_password(another_user: User) -> User:
    Password.objects.create(owner=another_user, value=hash_password(ANOTHER_USER_PASSWORD))

    return another_user


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


@pytest.fixture
def pdf_document() -> SimpleUploadedFile:
    return SimpleUploadedFile("test_document.pdf", b"123", content_type="application/pdf")
