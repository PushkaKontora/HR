from abc import ABC, abstractmethod
from typing import Iterable, Optional, Set

from django.db.models import QuerySet
from django.db.transaction import atomic
from django.utils.timezone import now
from ninja import UploadedFile

from api.internal.v1.resumes.db.sorters import IFavouriteResumeSorter
from api.internal.v1.resumes.domain.entities import (
    NewResumeIn,
    PublishingOut,
    ResumeIn,
    ResumeOut,
    ResumesOut,
    ResumesParams,
    ResumesSortBy,
    ResumesWishlistParameters,
)
from api.internal.v1.resumes.presentation.handlers import (
    ICreatingResumeService,
    IDocumentService,
    IGettingResumeService,
    IGettingResumesService,
    IPublishingResumeService,
    IResumesWishlistService,
    IUpdatingResumeService,
)
from api.models import Experience, FavouriteResume, Permission, Resume, User


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
        experience: Optional[Experience] = None,
        desired_salary: Optional[int] = None,
    ) -> Resume:
        pass

    @abstractmethod
    def get_published_at(self, resume_id: int) -> Resume:
        pass

    @abstractmethod
    def get_one_with_user_by_id(self, resume_id: int) -> Resume:
        pass

    @abstractmethod
    def exists_resume_with_id(self, resume_id: int) -> bool:
        pass

    @abstractmethod
    def get_one_by_id(self, resume_id: int) -> Resume:
        pass

    @abstractmethod
    def get_filtered_resumes(
        self,
        search: Optional[str],
        experience: Optional[Experience],
        salary_from: Optional[int],
        salary_to: Optional[int],
        competencies: Optional[Set[str]],
        published: Optional[bool],
    ) -> QuerySet[Resume]:
        pass


class ICompetencyRepository(ABC):
    @abstractmethod
    def get_existed_competencies_by_names(self, competencies: Set[str]) -> QuerySet[str]:
        pass


class IResumeCompetenciesRepository(ABC):
    @abstractmethod
    def attach_competencies_to_resume(self, resume_id: int, competencies: Set[str]) -> None:
        pass

    @abstractmethod
    def delete_all_competencies_from_resume(self, resume_id: int) -> None:
        pass


class IFavouriteResumeRepository(ABC):
    @abstractmethod
    def get_wishlist_with_resumes_and_resume_owners_and_competencies_by_user_id(
        self, user_id: int, sorter: IFavouriteResumeSorter
    ) -> QuerySet[FavouriteResume]:
        pass

    @abstractmethod
    def add_resume_to_wishlist(self, user_id: int, resume_id: int) -> None:
        pass

    @abstractmethod
    def exists_resume_in_user_wishlist(self, user_id: int, resume_id: int) -> bool:
        pass

    @abstractmethod
    def delete_resume_from_wishlist(self, user_id: int, resume_id: int) -> None:
        pass

    @abstractmethod
    def delete_resume_from_wishlists(self, resume_id: int) -> None:
        pass


class DocumentService(IDocumentService):
    def is_pdf(self, document: UploadedFile) -> bool:
        return document.content_type == "application/pdf"


class CreatingResumeService(ICreatingResumeService):
    def __init__(
        self,
        resume_repo: IResumeRepository,
        competency_repo: ICompetencyRepository,
        resume_competencies_repo: IResumeCompetenciesRepository,
    ):
        self.resume_competencies_repo = resume_competencies_repo
        self.competency_repo = competency_repo
        self.resume_repo = resume_repo

    def authorize(self, auth_user: User, extra: NewResumeIn) -> bool:
        return auth_user.id == extra.user_id

    def is_resume_created_by_user(self, extra: NewResumeIn) -> bool:
        return self.resume_repo.exists_resume_by_owner_id(extra.user_id)

    @atomic
    def create(self, extra: NewResumeIn, document: UploadedFile) -> None:
        resume = self.resume_repo.create(
            extra.user_id, document, extra.desired_job, extra.experience, extra.desired_salary
        )

        if extra.competencies:
            competencies = set(self.competency_repo.get_existed_competencies_by_names(set(extra.competencies)))
            self.resume_competencies_repo.attach_competencies_to_resume(resume.id, competencies)


class PublishingResumeService(IPublishingResumeService):
    def __init__(self, resume_repo: IResumeRepository, favourite_resume_repo: IFavouriteResumeRepository):
        self.favourite_resume_repo = favourite_resume_repo
        self.resume_repo = resume_repo

    def authorize(self, auth_user: User, resume_id: int) -> bool:
        return hasattr(auth_user, "resume") and auth_user.resume.id == resume_id

    def publish(self, resume_id: int) -> PublishingOut:
        resume = self.resume_repo.get_published_at(resume_id)

        if resume.published_at is None:
            resume.published_at = now()
            resume.save(update_fields=["published_at"])

        return PublishingOut.from_resume(resume)

    @atomic
    def unpublish(self, resume_id: int) -> None:
        resume = self.resume_repo.get_published_at(resume_id)

        if resume.published_at is not None:
            resume.published_at = None
            resume.save(update_fields=["published_at"])

        self.favourite_resume_repo.delete_resume_from_wishlists(resume_id)


class GettingResumeService(IGettingResumeService):
    def __init__(self, resume_repo: IResumeRepository):
        self.resume_repo = resume_repo

    def authorize(self, auth_user: User, resume_id: int) -> bool:
        is_employer = auth_user.permission == Permission.EMPLOYER
        is_owner = hasattr(auth_user, "resume") and auth_user.resume.id == resume_id

        return is_employer or is_owner

    def get_resume_out(self, resume_id: int) -> ResumeOut:
        return ResumeOut.from_resume(self.resume_repo.get_one_with_user_by_id(resume_id))

    def exists_resume_with_id(self, resume_id: int) -> bool:
        return self.resume_repo.exists_resume_with_id(resume_id)


class UpdatingResumeService(IUpdatingResumeService):
    def __init__(
        self,
        resume_repo: IResumeRepository,
        competency_repo: ICompetencyRepository,
        resume_competencies_repo: IResumeCompetenciesRepository,
    ):
        self.competency_repo = competency_repo
        self.resume_competencies_repo = resume_competencies_repo
        self.resume_repo = resume_repo

    def authorize(self, auth_user: User, resume_id: int) -> bool:
        return hasattr(auth_user, "resume") and auth_user.resume.id == resume_id

    @atomic
    def update(self, resume_id: int, extra: ResumeIn, document: Optional[UploadedFile]) -> None:
        resume = self.resume_repo.get_one_by_id(resume_id)

        resume.desired_job = extra.desired_job
        resume.desired_salary = extra.desired_salary
        resume.experience = extra.experience
        resume.document = document or resume.document
        resume.save()

        if extra.competencies:
            self.resume_competencies_repo.delete_all_competencies_from_resume(resume_id)

            competencies = set(self.competency_repo.get_existed_competencies_by_names(set(extra.competencies)))
            self.resume_competencies_repo.attach_competencies_to_resume(resume_id, competencies)


class ResumesWishlistService(IResumesWishlistService):
    def __init__(
        self,
        favourite_resume_repo: IFavouriteResumeRepository,
        resume_repo: IResumeRepository,
        resumes_published_at_asc_sorter: IFavouriteResumeSorter,
        resumes_wishlist_added_at_desc_sorter: IFavouriteResumeSorter,
    ):
        self.resume_repo = resume_repo
        self.favourite_resume_repo = favourite_resume_repo
        self.sorters = {
            ResumesSortBy.PUBLISHED_AT_ASC: resumes_published_at_asc_sorter,
            ResumesSortBy.ADDED_AT_DESC: resumes_wishlist_added_at_desc_sorter,
        }

    def authorize(self, auth_user: User) -> bool:
        return auth_user.permission == Permission.EMPLOYER

    def get_user_wishlist(self, auth_user: User, params: ResumesWishlistParameters) -> Iterable[ResumeOut]:
        favourites = self.favourite_resume_repo.get_wishlist_with_resumes_and_resume_owners_and_competencies_by_user_id(
            auth_user.id, self.sorters[params.sort_by]
        )

        return (ResumeOut.from_resume(favourite.resume) for favourite in favourites)

    def exists_resume_in_wishlist(self, auth_user: User, resume_id: int) -> bool:
        return self.favourite_resume_repo.exists_resume_in_user_wishlist(auth_user.id, resume_id)

    def add_resume_to_wishlist(self, auth_user: User, resume_id: int) -> None:
        self.favourite_resume_repo.add_resume_to_wishlist(auth_user.id, resume_id)

    def delete_resume_from_wishlist(self, auth_user: User, resume_id: int) -> None:
        self.favourite_resume_repo.delete_resume_from_wishlist(auth_user.id, resume_id)

    def is_resume_published(self, resume_id: int) -> bool:
        return self.resume_repo.get_published_at(resume_id).published_at is not None


class GettingResumesService(IGettingResumesService):
    def __init__(self, resume_repo: IResumeRepository):
        self.resume_repo = resume_repo

    def authorize(self, auth_user: User) -> bool:
        return auth_user.permission == Permission.EMPLOYER

    def get_resumes_out(self, params: ResumesParams) -> ResumesOut:
        offset, limit = params.offset, params.limit

        resumes = self.resume_repo.get_filtered_resumes(
            params.search,
            params.experience,
            params.salary_from,
            params.salary_to,
            params.competencies,
            params.published,
        )

        return ResumesOut.from_resumes_with_pagination(resumes, limit, offset)
