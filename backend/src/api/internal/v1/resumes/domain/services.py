from abc import ABC, abstractmethod
from typing import Optional, Set

from django.db.models import QuerySet
from django.db.transaction import atomic
from django.utils.timezone import now
from ninja import UploadedFile

from api.internal.v1.resumes.domain.entities import OwnerOut, PublishingOut, ResumeFormIn, ResumeOut
from api.internal.v1.resumes.presentation.handlers import (
    ICreatingResumeService,
    IGettingResumeService,
    IPublishingResumeService,
)
from api.models import Experiences, Permissions, Resume, User


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

    @abstractmethod
    def get_one_with_only_published_at(self, resume_id: int) -> Resume:
        pass

    @abstractmethod
    def get_one_with_user_by_id(self, resume_id: int) -> Resume:
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


class PublishingResumeService(IPublishingResumeService):
    def __init__(self, resume_repo: IResumeRepository):
        self.resume_repo = resume_repo

    def authorize(self, auth_user: User, resume_id: int) -> bool:
        return hasattr(auth_user, "resume") and auth_user.resume.id == resume_id

    def publish(self, resume_id: int) -> PublishingOut:
        resume = self.resume_repo.get_one_with_only_published_at(resume_id)

        if resume.published_at is None:
            resume.published_at = now()
            resume.save(update_fields=["published_at"])

        return PublishingOut(published_at=resume.published_at)

    def unpublish(self, resume_id: int) -> None:
        resume = self.resume_repo.get_one_with_only_published_at(resume_id)

        resume.published_at = None
        resume.save(update_fields=["published_at"])


class GettingResumeService(IGettingResumeService):
    def __init__(self, resume_repo: IResumeRepository):
        self.resume_repo = resume_repo

    def authorize(self, auth_user: User, resume_id: int) -> bool:
        is_employer = auth_user.permission == Permissions.EMPLOYER
        is_owner = hasattr(auth_user, "resume") and auth_user.resume.id == resume_id

        return is_employer or is_owner

    def get_resume_out(self, resume_id: int) -> ResumeOut:
        resume = self.resume_repo.get_one_with_user_by_id(resume_id)
        owner = resume.owner

        return ResumeOut(
            owner=OwnerOut(
                surname=owner.surname,
                name=owner.name,
                patronymic=owner.patronymic,
                email=owner.email,
            ),
            desired_job=resume.desired_job,
            desired_salary=resume.desired_salary,
            experience=resume.experience,
            document=resume.document.url,
            published_at=resume.published_at,
            competencies=list(resume.competencies.values_list("name", flat=True)),
        )
