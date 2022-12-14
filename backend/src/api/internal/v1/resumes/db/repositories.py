from typing import Iterable, Optional, Set

from django.db.models import QuerySet
from ninja import UploadedFile

from api.internal.v1.resumes.db.filters import IResumesFilter
from api.internal.v1.resumes.db.searchers import ResumesSearcherBase
from api.internal.v1.resumes.db.sorters import IWishlistSorter
from api.internal.v1.resumes.domain.services import (
    ICompetencyRepository,
    IFavouriteResumeRepository,
    IResumeCompetenciesRepository,
    IResumeRepository,
)
from api.models import Competency, Experience, FavouriteResume, Resume, ResumeCompetency


class ResumeRepository(IResumeRepository):
    def exists_resume_with_id(self, resume_id: int) -> bool:
        return Resume.objects.filter(id=resume_id).exists()

    def get_resume_by_id(self, resume_id: int) -> Resume:
        return Resume.objects.get(id=resume_id)

    def exists_resume_by_owner_id(self, owner_id: int) -> bool:
        return Resume.objects.filter(owner_id=owner_id).exists()

    def create(
        self,
        owner_id: int,
        document: Optional[UploadedFile],
        desired_job: Optional[str],
        experience: Optional[Experience] = None,
        desired_salary: Optional[int] = None,
    ) -> Resume:
        return Resume.objects.create(
            owner_id=owner_id,
            document=document,
            desired_job=desired_job,
            experience=experience,
            desired_salary=desired_salary,
        )

    def get_resume_for_update_with_only_published_at(self, resume_id: int) -> Resume:
        return Resume.objects.only("published_at").select_for_update().get(id=resume_id)

    def get_resume_with_user_by_id(self, resume_id: int) -> Resume:
        return Resume.objects.select_related("owner").get(id=resume_id)

    def get_resumes(self, filters: Iterable[IResumesFilter], searcher: ResumesSearcherBase) -> QuerySet[Resume]:
        resumes = Resume.objects.all()

        for obj in filters:
            resumes = obj.filter(resumes)

        return searcher.search(resumes)

    def get_resume_for_update(self, resume_id: int) -> Resume:
        return Resume.objects.select_for_update().get(id=resume_id)

    def get_resume_with_only_published_at(self, resume_id: int) -> Resume:
        return Resume.objects.only("published_at").get(id=resume_id)


class CompetencyRepository(ICompetencyRepository):
    def get_existed_competencies_by_names(self, competencies: Set[str]) -> QuerySet[str]:
        return Competency.objects.filter(name__in=competencies).values_list("name", flat=True)


class ResumeCompetenciesRepository(IResumeCompetenciesRepository):
    def delete_all_competencies_from_resume(self, resume_id: int) -> None:
        ResumeCompetency.objects.filter(resume_id=resume_id).delete()

    def attach_competencies_to_resume(self, resume_id: int, competencies: Set[str]) -> None:
        ResumeCompetency.objects.bulk_create(
            ResumeCompetency(resume_id=resume_id, competency_id=competency) for competency in competencies
        )


class FavouriteResumeRepository(IFavouriteResumeRepository):
    def get_wishlist_with_resumes_and_resume_owners_and_competencies_by_user_id(
        self, user_id: int, sorter: IWishlistSorter
    ) -> QuerySet[FavouriteResume]:
        wishlist = (
            FavouriteResume.objects.select_related("resume")
            .select_related("resume__owner")
            .prefetch_related("resume__competencies")
            .filter(user_id=user_id)
        )

        return sorter.sort(wishlist)

    def add_resume_to_wishlist(self, user_id: int, resume_id: int) -> None:
        FavouriteResume.objects.get_or_create(user_id=user_id, resume_id=resume_id)

    def exists_resume_in_user_wishlist(self, user_id: int, resume_id: int) -> bool:
        return FavouriteResume.objects.filter(user_id=user_id, resume_id=resume_id).exists()

    def delete_resume_from_wishlist(self, user_id: int, resume_id: int) -> None:
        FavouriteResume.objects.filter(user_id=user_id, resume_id=resume_id).delete()

    def delete_resume_from_wishlists(self, resume_id: int) -> None:
        FavouriteResume.objects.filter(resume_id=resume_id).delete()
