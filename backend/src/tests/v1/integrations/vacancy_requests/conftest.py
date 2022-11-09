from typing import Optional

from api.models import VacancyRequest
from tests.v1.integrations.conftest import V1, datetime_to_string

VACANCY_REQUESTS = V1 + "/vacancy-requests"


def request_out(request: Optional[VacancyRequest]) -> dict:
    return {"id": request.id, "created_at": datetime_to_string(request.created_at)}
