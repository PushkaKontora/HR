from datetime import datetime
from typing import Iterable, Optional

from django.db.models import QuerySet

from api.internal.v1.vacancies.db.filters import IVacanciesFilter
from api.internal.v1.vacancies.db.searchers import VacanciesBaseSearcher
from api.internal.v1.vacancies.db.sorters import IVacanciesWishlistSorter, VacanciesBaseSorter
from api.internal.v1.vacancies.domain.services import (
    IDepartmentRepository,
    IFavouriteVacancyRepository,
    IVacancyRepository,
)
from api.models import Department, Experience, FavouriteVacancy, User, Vacancy, VacancyRequest


class VacancyRepository(IVacancyRepository):
    def create(
        self,
        department_id: int,
        name: str,
        description: str,
        expected_experience: Experience,
        salary_to: Optional[int],
        salary_from: Optional[int],
        published_at: Optional[datetime],
    ) -> Vacancy:
        return Vacancy.objects.create(
            department_id=department_id,
            name=name,
            description=description,
            expected_experience=expected_experience,
            salary_from=salary_from,
            salary_to=salary_to,
            published_at=published_at,
        )

    def try_get_vacancy_by_id(self, vacancy_id: int) -> Optional[Vacancy]:
        return Vacancy.objects.filter(id=vacancy_id).first()

    def exists_vacancy_with_id(self, vacancy_id: int) -> bool:
        return Vacancy.objects.filter(id=vacancy_id).exists()

    def is_vacancy_owned(self, vacancy_id: int, employer_id: int) -> bool:
        return Vacancy.objects.filter(id=vacancy_id, department__leader_id=employer_id).exists()

    def set_published_at_to_vacancy_by_id(self, vacancy_id: int, published_at: Optional[datetime]) -> None:
        Vacancy.objects.filter(id=vacancy_id).update(published_at=published_at)

    def get_only_published_at_by_id(self, vacancy_id: int) -> Vacancy:
        return Vacancy.objects.only("published_at").get(id=vacancy_id)

    def exists_vacancy_with_id_and_leader_of_department_id(self, vacancy_id: int, leader_id: int) -> bool:
        return Vacancy.objects.filter(id=vacancy_id, department__leader_id=leader_id).exists()

    def update(
        self,
        vacancy_id: int,
        name: str,
        description: Optional[str],
        expected_experience: Experience,
        salary_to: Optional[int],
        salary_from: Optional[int],
        published_at: Optional[datetime],
    ) -> None:
        Vacancy.objects.filter(id=vacancy_id).update(
            name=name,
            description=description,
            expected_experience=expected_experience,
            salary_from=salary_from,
            salary_to=salary_to,
            published_at=published_at,
        )

    def get_filtered_vacancies(
        self, filters: Iterable[IVacanciesFilter], searcher: VacanciesBaseSearcher, sorter: VacanciesBaseSorter
    ) -> QuerySet[Vacancy]:
        vacancies = Vacancy.objects.all()

        for obj in filters:
            vacancies = obj.filter(vacancies)

        return searcher.search(sorter.sort(vacancies))


class DepartmentRepository(IDepartmentRepository):
    def exists_department_with_id(self, department_id: int) -> bool:
        return Department.objects.filter(id=department_id).exists()


class FavouriteVacancyRepository(IFavouriteVacancyRepository):
    def get_sorted_wishlist_with_vacancies_and_departments_and_leaders_by_user_id(
        self, user_id: int, sorter: IVacanciesWishlistSorter
    ) -> QuerySet[FavouriteVacancy]:
        wishlist = FavouriteVacancy.objects.select_related(
            "vacancy", "vacancy__department", "vacancy__department__leader"
        ).filter(user_id=user_id)

        return sorter.sort(wishlist)

    def exists_vacancy_in_wishlist(self, user_id: int, vacancy_id: int) -> bool:
        return FavouriteVacancy.objects.filter(user_id=user_id, vacancy_id=vacancy_id).exists()

    def add_vacancy_to_wishlist(self, user_id: int, vacancy_id: int) -> None:
        FavouriteVacancy.objects.create(user_id=user_id, vacancy_id=vacancy_id)

    def delete_vacancy_from_all_wishlists(self, vacancy_id: int) -> None:
        FavouriteVacancy.objects.filter(vacancy_id=vacancy_id).delete()

    def delete_vacancy_from_wishlist(self, user_id: int, vacancy_id: int) -> None:
        FavouriteVacancy.objects.filter(user_id=user_id, vacancy_id=vacancy_id).delete()
