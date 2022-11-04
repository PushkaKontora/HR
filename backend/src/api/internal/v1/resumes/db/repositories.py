from typing import List, Optional, Set

from django.db.models import QuerySet
from ninja import UploadedFile

from api.internal.v1.resumes.db.searchers import IResumesSearcher
from api.internal.v1.resumes.db.sorters import FavouriteResumeSorter
from api.internal.v1.resumes.domain.services import (
    ICompetencyRepository,
    IFavouriteResumeRepository,
    IResumeCompetenciesRepository,
    IResumeRepository,
)
from api.models import Competency, Experience, FavouriteResume, Resume, ResumeCompetency


class ResumeRepository(IResumeRepository):
    def __init__(
        self,
        desired_job_searcher: IResumesSearcher,
        experience_searcher: IResumesSearcher,
        salary_from_searcher: IResumesSearcher,
        salary_to_searcher: IResumesSearcher,
        competencies_searcher: IResumesSearcher,
    ):
        self.desired_job_searcher = desired_job_searcher
        self.experience_searcher = experience_searcher
        self.salary_from_searcher = salary_from_searcher
        self.salary_to_searcher = salary_to_searcher
        self.competencies_searcher = competencies_searcher

    def exists_resume_with_id(self, resume_id: int) -> bool:
        return Resume.objects.filter(id=resume_id).exists()

    def get_one_by_id(self, resume_id: int) -> Resume:
        return Resume.objects.get(id=resume_id)

    def exists_resume_by_owner_id(self, owner_id: int) -> bool:
        return Resume.objects.filter(owner_id=owner_id).exists()

    def create(
        self,
        owner_id: int,
        document: UploadedFile,
        desired_job: str,
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

    def get_one_with_only_published_at(self, resume_id: int) -> Resume:
        return Resume.objects.only("published_at").get(id=resume_id)

    def get_one_with_user_by_id(self, resume_id: int) -> Resume:
        return Resume.objects.select_related("owner").get(id=resume_id)

    def get_filtered_resumes(
        self,
        search: Optional[str],
        experience: Optional[Experience],
        salary_from: Optional[int],
        salary_to: Optional[int],
        competencies: Optional[Set[str]],
    ) -> QuerySet[Resume]:
        searchers = {
            self.desired_job_searcher: search,
            self.experience_searcher: experience,
            self.salary_from_searcher: salary_from,
            self.salary_to_searcher: salary_to,
            self.competencies_searcher: competencies,
        }

        queryset = Resume.objects.all()

        for searcher, value in searchers.items():
            queryset = queryset if value is None else searcher.search(queryset, value)

        return queryset


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
    def get_all_with_resume_and_resume_owner_and_competencies_by_user_id(
        self, user_id: int, sorter: FavouriteResumeSorter
    ) -> QuerySet[FavouriteResume]:
        queryset = (
            FavouriteResume.objects.select_related("resume")
            .select_related("resume__owner")
            .prefetch_related("resume__competencies")
            .filter(user_id=user_id)
        )

        return sorter.execute(queryset)

    def add_resume_to_wishlist(self, user_id: int, resume_id: int) -> None:
        FavouriteResume.objects.create(user_id=user_id, resume_id=resume_id)

    def exists_resume_in_user_wishlist(self, user_id: int, resume_id: int) -> bool:
        return FavouriteResume.objects.filter(user_id=user_id, resume_id=resume_id).exists()

    def delete_resume_from_wishlist(self, user_id: int, resume_id: int) -> None:
        FavouriteResume.objects.filter(user_id=user_id, resume_id=resume_id).delete()
