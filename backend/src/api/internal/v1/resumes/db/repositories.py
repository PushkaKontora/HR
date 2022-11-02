from typing import Optional, Set

from django.db.models import QuerySet
from ninja import UploadedFile

from api.internal.v1.resumes.domain.services import (
    ICompetencyRepository,
    IResumeCompetenciesRepository,
    IResumeRepository,
)
from api.models import Competency, Experiences, Resume, ResumeCompetency


class ResumeRepository(IResumeRepository):
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
        experience: Optional[Experiences] = None,
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
