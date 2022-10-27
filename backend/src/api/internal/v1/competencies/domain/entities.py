from typing import Optional

from ninja import Schema


class CompetenciesFilters(Schema):
    search: Optional[str] = None


class CompetencyOut(Schema):
    name: str
