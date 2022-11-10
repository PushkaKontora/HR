from abc import ABC, abstractmethod

from django.db.models import Case, F, Max, Min, PositiveIntegerField, QuerySet, Value, When

from api.models import FavouriteVacancy, Vacancy


class VacanciesBaseSorter(ABC):
    @abstractmethod
    def sort(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        pass


class VacanciesSortByNameASC(VacanciesBaseSorter):
    def sort(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        return vacancies.order_by("name")


class VacanciesSortByPublishedAtDESC(VacanciesBaseSorter):
    def sort(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        return vacancies.order_by(F("published_at").desc(nulls_last=True))


class VacanciesSortBySalaryAtEndsASC(VacanciesBaseSorter):
    def sort(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        return vacancies.order_by(F("salary_from").asc(nulls_last=True), F("salary_to").asc(nulls_last=True))


class VacanciesSortBySalaryAtEndsDESC(VacanciesBaseSorter):
    def sort(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        return vacancies.order_by(F("salary_from").desc(nulls_last=True), F("salary_to").desc(nulls_last=True))


class VacanciesSortByAverageSalaryBase(VacanciesBaseSorter, ABC):
    @abstractmethod
    def sort(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        pass

    @staticmethod
    def prepare_queryset(vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        limits = vacancies.aggregate(min=Min("salary_from"), max=Max("salary_to"))
        min_salary_from, max_salary_to = limits["min"], limits["max"]

        salary_from = Case(
            When(salary_from=None, then=Value(min_salary_from)),
            default="salary_from",
            output_field=PositiveIntegerField(),
        )
        salary_to = Case(
            When(salary_to=None, then=Value(max_salary_to)), default="salary_to", output_field=PositiveIntegerField()
        )

        return vacancies.annotate(salary=(salary_from + salary_to) / Value(2.0))


class VacanciesSortByAverageSalaryASC(VacanciesSortByAverageSalaryBase):
    def sort(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        return self.prepare_queryset(vacancies).order_by("salary")


class VacanciesSortByAverageSalaryDESC(VacanciesSortByAverageSalaryBase):
    def sort(self, vacancies: QuerySet[Vacancy]) -> QuerySet[Vacancy]:
        return self.prepare_queryset(vacancies).order_by("-salary")


class IVacanciesWishlistSorter(ABC):
    @abstractmethod
    def sort(self, favourites: QuerySet[FavouriteVacancy]) -> QuerySet[FavouriteVacancy]:
        pass


class VacanciesWishlistSortByPublishedAtASC(IVacanciesWishlistSorter):
    def sort(self, favourites: QuerySet[FavouriteVacancy]) -> QuerySet[FavouriteVacancy]:
        return favourites.order_by("vacancy__published_at")


class VacanciesWishlistSortByAddedAtDESC(IVacanciesWishlistSorter):
    def sort(self, favourites: QuerySet[FavouriteVacancy]) -> QuerySet[FavouriteVacancy]:
        return favourites.order_by("-added_at")
