from abc import ABC, abstractmethod

from django.db.models import QuerySet

from api.models import FavouriteResume


class FavouriteResumeSorter(ABC):
    @abstractmethod
    def execute(self, resumes: QuerySet[FavouriteResume]) -> QuerySet[FavouriteResume]:
        pass


class SortByPublishedAtASC(FavouriteResumeSorter):
    def execute(self, favourites: QuerySet[FavouriteResume]) -> QuerySet[FavouriteResume]:
        return favourites.order_by("resume__published_at")


class SortByAddedAtDESC(FavouriteResumeSorter):
    def execute(self, favourites: QuerySet[FavouriteResume]) -> QuerySet[FavouriteResume]:
        return favourites.order_by("-added_at")
