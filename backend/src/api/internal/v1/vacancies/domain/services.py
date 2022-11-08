from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable, Optional

from django.db.models import QuerySet
from django.db.transaction import atomic
from django.utils.timezone import now

from api.internal.v1.vacancies.db.sorters import IVacanciesWishlistSorter
from api.internal.v1.vacancies.domain.entities import (
    NewVacancyIn,
    PublishingOut,
    VacanciesWishlistParams,
    VacanciesWishlistSortBy,
    VacancyOut,
)
from api.internal.v1.vacancies.presentation.handlers import (
    ICreatingVacancyService,
    IGettingService,
    IPublishingVacancyService,
    IUpdatingVacancyService,
    IVacanciesWishlistService,
)
from api.models import Experience, FavouriteVacancy, Permission, User, Vacancy


class IVacancyRepository(ABC):
    @abstractmethod
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
        pass

    @abstractmethod
    def try_get_vacancy_by_id(self, vacancy_id: int) -> Optional[Vacancy]:
        pass

    @abstractmethod
    def exists_vacancy_with_id(self, vacancy_id: int) -> bool:
        pass

    @abstractmethod
    def is_vacancy_owned(self, vacancy_id: int, employer_id: int) -> bool:
        pass

    @abstractmethod
    def set_published_at_to_vacancy_by_id(self, vacancy_id: int, published_at: Optional[datetime]) -> None:
        pass

    @abstractmethod
    def get_only_published_at_by_id(self, vacancy_id: int) -> Vacancy:
        pass

    @abstractmethod
    def exists_vacancy_with_id_and_leader_of_department_id(self, vacancy_id: int, leader_id: int) -> bool:
        pass

    @abstractmethod
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
        pass


class IDepartmentRepository(ABC):
    @abstractmethod
    def exists_department_with_id(self, department_id: int) -> bool:
        pass


class IFavouriteVacancyRepository(ABC):
    @abstractmethod
    def get_sorted_wishlist_with_vacancies_and_departments_and_leaders_by_user_id(
        self, user_id: int, sorter: IVacanciesWishlistSorter
    ) -> QuerySet[FavouriteVacancy]:
        pass

    @abstractmethod
    def exists_vacancy_in_wishlist(self, user_id: int, vacancy_id: int) -> bool:
        pass

    @abstractmethod
    def add_vacancy_to_wishlist(self, user_id: int, vacancy_id: int) -> None:
        pass

    @abstractmethod
    def delete_vacancy_from_all_wishlists(self, vacancy_id: int) -> None:
        pass

    @abstractmethod
    def delete_vacancy_from_wishlist(self, user_id: int, vacancy_id: int) -> None:
        pass


class CreatingVacancyService(ICreatingVacancyService):
    def __init__(self, vacancy_repo: IVacancyRepository, department_repo: IDepartmentRepository):
        self.department_repo = department_repo
        self.vacancy_repo = vacancy_repo

    def exists_department_with_id(self, department_id: int) -> bool:
        return self.department_repo.exists_department_with_id(department_id)

    def authorize(self, auth_user: User, body: NewVacancyIn) -> bool:
        is_employer = auth_user.permission == Permission.EMPLOYER
        is_leader = hasattr(auth_user, "department") and auth_user.department.id == body.department_id

        return is_employer and is_leader

    def create(self, body: NewVacancyIn) -> None:
        self.vacancy_repo.create(
            body.department_id,
            body.name,
            body.description,
            body.expected_experience,
            body.salary_to,
            body.salary_from,
            published_at=now() if body.published else None,
        )


class GettingService(IGettingService):
    def __init__(self, vacancy_repo: IVacancyRepository):
        self.vacancy_repo = vacancy_repo

    def try_get_vacancy_out_by_id(self, vacancy_id: int) -> Optional[VacancyOut]:
        vacancy = self.vacancy_repo.try_get_vacancy_by_id(vacancy_id)

        if not vacancy:
            return None

        return VacancyOut.from_vacancy(vacancy)

    def exists_vacancy_with_id(self, vacancy_id: int) -> bool:
        return self.vacancy_repo.exists_vacancy_with_id(vacancy_id)

    def is_published(self, vacancy_id: int) -> bool:
        return self.vacancy_repo.get_only_published_at_by_id(vacancy_id).published_at is not None


class PublishingVacancyService(IPublishingVacancyService):
    def __init__(self, vacancy_repo: IVacancyRepository, favourite_vacancy_repo: IFavouriteVacancyRepository):
        self.favourite_vacancy_repo = favourite_vacancy_repo
        self.vacancy_repo = vacancy_repo

    def authorize(self, auth_user: User, vacancy_id: int) -> bool:
        is_employer = auth_user.permission == Permission.EMPLOYER
        is_leader = hasattr(auth_user, "department") and self.vacancy_repo.is_vacancy_owned(vacancy_id, auth_user.id)

        return is_employer and is_leader

    def publish(self, vacancy_id: int) -> PublishingOut:
        vacancy = self.vacancy_repo.get_only_published_at_by_id(vacancy_id)
        published_at = vacancy.published_at or now()

        self.vacancy_repo.set_published_at_to_vacancy_by_id(vacancy_id, published_at)

        return PublishingOut.create(published_at)

    @atomic
    def unpublish(self, vacancy_id: int) -> None:
        self.vacancy_repo.set_published_at_to_vacancy_by_id(vacancy_id, None)
        self.favourite_vacancy_repo.delete_vacancy_from_all_wishlists(vacancy_id)


class VacanciesWishlistService(IVacanciesWishlistService):
    def __init__(
        self,
        favourite_vacancy_repo: IFavouriteVacancyRepository,
        published_at_asc_sorter: IVacanciesWishlistSorter,
        added_at_desc_sorter: IVacanciesWishlistSorter,
    ):
        self.favourite_vacancy_repo = favourite_vacancy_repo
        self.sorters = {
            VacanciesWishlistSortBy.PUBLISHED_AT_ASC: published_at_asc_sorter,
            VacanciesWishlistSortBy.ADDED_AT_DESC: added_at_desc_sorter,
        }

    def get_user_wishlist(self, auth_user: User, params: VacanciesWishlistParams) -> Iterable[VacancyOut]:
        wishlist = (
            self.favourite_vacancy_repo.get_sorted_wishlist_with_vacancies_and_departments_and_leaders_by_user_id(
                auth_user.id, self.sorters[params.sort_by]
            )
        )

        return (VacancyOut.from_vacancy(favourite.vacancy) for favourite in wishlist)

    def exists_vacancy_in_wishlist(self, auth_user: User, vacancy_id: int) -> bool:
        return self.favourite_vacancy_repo.exists_vacancy_in_wishlist(auth_user.id, vacancy_id)

    def add_vacancy_to_wishlist(self, auth_user: User, vacancy_id: int) -> None:
        self.favourite_vacancy_repo.add_vacancy_to_wishlist(auth_user.id, vacancy_id)

    def delete_vacancy_from_wishlist(self, auth_user: User, vacancy_id: int) -> None:
        self.favourite_vacancy_repo.delete_vacancy_from_wishlist(auth_user.id, vacancy_id)


class UpdatingVacancyService(IUpdatingVacancyService):
    def __init__(self, vacancy_repo: IVacancyRepository):
        self.vacancy_repo = vacancy_repo

    def authorize(self, auth_user: User, vacancy_id: int) -> bool:
        return hasattr(auth_user, "department") and self.vacancy_repo.exists_vacancy_with_id_and_leader_of_department_id(
            vacancy_id, auth_user.id
        )

    def update_vacancy(self, vacancy_id: int, body: NewVacancyIn) -> None:
        self.vacancy_repo.update(
            vacancy_id,
            body.name,
            body.description,
            body.expected_experience,
            body.salary_to,
            body.salary_from,
            published_at=now() if body.published else None,
        )
