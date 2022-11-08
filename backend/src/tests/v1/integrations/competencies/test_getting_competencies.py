import pytest
from django.test import Client
from ninja.responses import Response

from api.models import Competency
from tests.v1.integrations.competencies.conftest import COMPETENCIES
from tests.v1.integrations.conftest import get


def get_all(client: Client) -> Response:
    return get(client, COMPETENCIES)


def competency_out(competency: Competency) -> dict:
    return {"name": competency.name}


@pytest.mark.integration
@pytest.mark.django_db
def test_get_competencies(client: Client, competencies_names=("redux", "angular")) -> None:
    competencies = Competency.objects.bulk_create(Competency(name=name) for name in competencies_names)

    response = get_all(client)

    assert response.status_code == 200
    assert response.json() == [competency_out(competency) for competency in competencies]
