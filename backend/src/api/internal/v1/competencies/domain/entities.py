from ninja import Schema

from api.models import Competency


class CompetencyOut(Schema):
    name: str

    @staticmethod
    def from_competency(competency: Competency) -> "CompetencyOut":
        return CompetencyOut(name=competency.name)
