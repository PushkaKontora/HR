from abc import ABC, abstractmethod
from typing import Iterable, List, Type

from api.internal.v1.resumes.db.filters import (
    CompetenciesFilterBase,
    ExperienceFilterBase,
    IResumesFilter,
    PublishedFilterBase,
    SalaryFilterBase,
)
from api.internal.v1.resumes.db.searchers import ResumesSearcherBase
from api.internal.v1.resumes.db.sorters import IWishlistSorter
from api.internal.v1.resumes.domain.entities import ResumesQueryParams, ResumesSortBy


class IResumesFiltersBuilder(ABC):
    @abstractmethod
    def build(self, params: ResumesQueryParams) -> List[IResumesFilter]:
        pass


class IResumesSearcherBuilder(ABC):
    @abstractmethod
    def build(self, params: ResumesQueryParams) -> ResumesSearcherBase:
        pass


class IWishlistSorterBuilder(ABC):
    @abstractmethod
    def build(self, sort_by: ResumesSortBy) -> IWishlistSorter:
        pass


class ResumesFiltersBuilder(IResumesFiltersBuilder):
    def __init__(
        self,
        experience_filter_cls: Type[ExperienceFilterBase],
        salary_filter_cls: Type[SalaryFilterBase],
        competencies_filter_cls: Type[CompetenciesFilterBase],
        published_filter_cls: Type[PublishedFilterBase],
    ):
        self.published_filter_cls = published_filter_cls
        self.competencies_filter_cls = competencies_filter_cls
        self.salary_filter_cls = salary_filter_cls
        self.experience_filter_cls = experience_filter_cls

    def build(self, params: ResumesQueryParams) -> List[IResumesFilter]:
        return list(self._build(params))

    def _build(self, params: ResumesQueryParams) -> Iterable[IResumesFilter]:
        yield self.experience_filter_cls(params.experience)
        yield self.salary_filter_cls(params.salary_from, params.salary_to)
        yield self.competencies_filter_cls(params.competencies)
        yield self.published_filter_cls(params.published)


class ResumesSearcherBuilder(IResumesSearcherBuilder):
    def __init__(self, searcher_cls: Type[ResumesSearcherBase]):
        self.searcher_cls = searcher_cls

    def build(self, params: ResumesQueryParams) -> ResumesSearcherBase:
        return self.searcher_cls(params.search)


class WishlistSorterBuilder(IWishlistSorterBuilder):
    def __init__(
        self,
        published_at_asc_sorter_cls: Type[IWishlistSorter],
        added_at_desc_sorter_cls: Type[IWishlistSorter],
        published_at_desc_sorter_cls: Type[IWishlistSorter],
    ):
        self.sorters = {
            ResumesSortBy.PUBLISHED_AT_ASC: published_at_asc_sorter_cls,
            ResumesSortBy.ADDED_AT_DESC: added_at_desc_sorter_cls,
            ResumesSortBy.PUBLISHED_AT_DESC: published_at_desc_sorter_cls,
        }

    def build(self, sort_by: ResumesSortBy) -> IWishlistSorter:
        return self.sorters[sort_by]()
