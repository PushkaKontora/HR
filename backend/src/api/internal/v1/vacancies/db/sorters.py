from abc import ABC, abstractmethod

from django.db.models import QuerySet

from api.models import FavouriteVacancy


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
