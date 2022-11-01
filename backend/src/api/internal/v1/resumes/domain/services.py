from abc import ABC, abstractmethod
from typing import Optional, Set

from django.db.models import QuerySet
from django.db.transaction import atomic
from ninja import UploadedFile

from api.internal.v1.resumes.domain.entities import ResumeFormIn
from api.internal.v1.resumes.presentation.handlers import ICreatingResumeService
from api.models import Experiences, Resume, User


class IResumeRepository(ABC):
    @abstractmethod
    def exists_resume_by_owner_id(self, owner_id: int) -> bool:
        pass

    @abstractmethod
    def create(
        self,
        owner_id: int,
        document: UploadedFile,
        desired_job: str,
        experience: Optional[Experiences] = None,
        desired_salary: Optional[int] = None,
    ) -> Resume:
        pass


class ICompetencyRepository(ABC):
    @abstractmethod
    def get_existed_competencies_by_names(self, competencies: Set[str]) -> QuerySet[str]:
        pass


class IResumeCompetenciesRepository(ABC):
    @abstractmethod
    def attach_competencies_to_resume(self, resume_id: int, competencies: Set[str]) -> None:
        pass


class CreatingResumeService(ICreatingResumeService):
    PDF_MIME_TYPE = "application/pdf"

    def __init__(
        self,
        resume_repo: IResumeRepository,
        competency_repo: ICompetencyRepository,
        resume_competencies_repo: IResumeCompetenciesRepository,
    ):
        self.resume_competencies_repo = resume_competencies_repo
        self.competency_repo = competency_repo
        self.resume_repo = resume_repo

    def is_pdf(self, document: UploadedFile) -> bool:
        return document.content_type == self.PDF_MIME_TYPE

    def authorize(self, auth_user: User, extra: ResumeFormIn) -> bool:
        return auth_user.id == extra.user_id

    def is_resume_created_by_user(self, extra: ResumeFormIn) -> bool:
        return self.resume_repo.exists_resume_by_owner_id(extra.user_id)

    @atomic
    def create(self, extra: ResumeFormIn, document: UploadedFile) -> None:
        resume = self.resume_repo.create(
            extra.user_id, document, extra.desired_job, extra.experience, extra.desired_salary
        )

        if extra.competencies:
            competencies = set(self.competency_repo.get_existed_competencies_by_names(set(extra.competencies)))
            self.resume_competencies_repo.attach_competencies_to_resume(resume.id, competencies)
