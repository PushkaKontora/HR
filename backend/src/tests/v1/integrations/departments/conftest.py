import pytest

from api.models import Department, User
from tests.v1.integrations.conftest import V1

DEPARTMENTS = V1 + "/departments"
DEPARTMENT = DEPARTMENTS + "/{department_id}"


@pytest.fixture
def department(employer: User) -> Department:
    return Department.objects.create(leader=employer, name="123")
