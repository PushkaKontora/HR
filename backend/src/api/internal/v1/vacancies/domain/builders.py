from abc import ABC, abstractmethod
from typing import Iterable, List, Type

from api.internal.v1.vacancies.db.filters import (
    DepartmentBaseFilter,
    ExperienceBaseFilter,
    IVacanciesFilter,
    PublishedBaseFilter,
    SalaryBaseFilter,
)
from api.internal.v1.vacancies.db.searchers import VacanciesBaseSearcher
from api.internal.v1.vacancies.db.sorters import VacanciesBaseSorter
from api.internal.v1.vacancies.domain.entities import VacanciesParams, VacanciesSortBy


class IFilterBuilder(ABC):
    @abstractmethod
    def build(self, params: VacanciesParams) -> List[IVacanciesFilter]:
        pass


class ISearcherBuilder(ABC):
    @abstractmethod
    def build(self, params: VacanciesParams) -> VacanciesBaseSearcher:
        pass


class ISorterBuilder(ABC):
    @abstractmethod
    def build(self, params: VacanciesParams) -> VacanciesBaseSorter:
        pass


class VacanciesFiltersBuilder(IFilterBuilder):
    def __init__(
        self,
        department_filter_cls: Type[DepartmentBaseFilter],
        experience_filter_cls: Type[ExperienceBaseFilter],
        salary_filter_cls: Type[SalaryBaseFilter],
        published_filter_cls: Type[PublishedBaseFilter],
    ):
        self.published_filter_cls = published_filter_cls
        self.salary_filter_cls = salary_filter_cls
        self.experience_filter_cls = experience_filter_cls
        self.department_filter_cls = department_filter_cls

    def build(self, params: VacanciesParams) -> List[IVacanciesFilter]:
        return list(self._build(params))

    def _build(self, params: VacanciesParams) -> Iterable[IVacanciesFilter]:
        yield self.published_filter_cls(params.published)
        yield self.salary_filter_cls(params.salary_from, params.salary_to)
        yield self.experience_filter_cls(params.experience)
        yield self.department_filter_cls(params.department_id)


class VacanciesSearcherBuilder(ISearcherBuilder):
    def __init__(self, searcher_cls: Type[VacanciesBaseSearcher]):
        self.searcher_cls = searcher_cls

    def build(self, params: VacanciesParams) -> VacanciesBaseSearcher:
        return self.searcher_cls(params.search)


class VacanciesSorterBuilder(ISorterBuilder):
    def __init__(
        self,
        name_asc_sorter_cls: Type[VacanciesBaseSorter],
        published_at_desc_sorter_cls: Type[VacanciesBaseSorter],
        salary_asc_sorter_cls: Type[VacanciesBaseSorter],
        salary_desc_sorter_cls: Type[VacanciesBaseSorter],
    ):
        self.sorters = {
            VacanciesSortBy.NAME_ASC: name_asc_sorter_cls,
            VacanciesSortBy.PUBLISHED_AT_DESC: published_at_desc_sorter_cls,
            VacanciesSortBy.SALARY_ASC: salary_asc_sorter_cls,
            VacanciesSortBy.SALARY_DESC: salary_desc_sorter_cls,
        }

    def build(self, params: VacanciesParams) -> VacanciesBaseSorter:
        return self.sorters[params.sort_by]()
