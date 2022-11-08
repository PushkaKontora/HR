from abc import ABC, abstractmethod

from django.db.models import QuerySet

from api.models import FavouriteResume


class IFavouriteResumeSorter(ABC):
    @abstractmethod
    def sort(self, resumes: QuerySet[FavouriteResume]) -> QuerySet[FavouriteResume]:
        pass


class ResumesPublishedAtASCSorter(IFavouriteResumeSorter):
    def sort(self, favourites: QuerySet[FavouriteResume]) -> QuerySet[FavouriteResume]:
        return favourites.order_by("resume__published_at")


class ResumesWishlistAddedAtDESCSorter(IFavouriteResumeSorter):
    def sort(self, favourites: QuerySet[FavouriteResume]) -> QuerySet[FavouriteResume]:
        return favourites.order_by("-added_at")
