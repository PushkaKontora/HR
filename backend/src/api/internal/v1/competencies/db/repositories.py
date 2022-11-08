from django.db.models import QuerySet

from api.internal.v1.competencies.domain.services import ICompetencyRepository
from api.models import Competency


class CompetencyRepository(ICompetencyRepository):
    def get_all(self) -> QuerySet[Competency]:
        return Competency.objects.all()
