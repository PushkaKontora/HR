from datetime import datetime

from ninja import Schema

from api.models import VacancyRequest


class RequestIn(Schema):
    vacancy_id: int
    desired_job: str


class RequestOut(Schema):
    id: int
    created_at: datetime

    @staticmethod
    def from_request(request: VacancyRequest) -> "RequestOut":
        return RequestOut(id=request.id, created_at=request.created_at)
