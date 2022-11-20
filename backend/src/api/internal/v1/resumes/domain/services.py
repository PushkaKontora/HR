import uuid
from abc import ABC, abstractmethod
from typing import Iterable, Optional, Set

from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models import QuerySet
from django.db.transaction import atomic
from django.utils.timezone import now
from ninja import UploadedFile

from api.internal.v1.resumes.db.filters import IResumesFilter
from api.internal.v1.resumes.db.searchers import ResumesSearcherBase
from api.internal.v1.resumes.db.sorters import IWishlistSorter
from api.internal.v1.resumes.domain.builders import (
    IResumesFiltersBuilder,
    IResumesSearcherBuilder,
    IWishlistSorterBuilder,
)
from api.internal.v1.resumes.domain.entities import (
    NewResumeIn,
    PublishingOut,
    ResumeIn,
    ResumeOut,
    ResumesOut,
    ResumesQueryParams,
    ResumesSortBy,
    ResumesWishlistQueryParams,
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
    def get_resume_for_update_with_only_published_at(self, resume_id: int) -> Resume:
        pass

    @abstractmethod
    def get_resume_with_user_by_id(self, resume_id: int) -> Resume:
        pass

    @abstractmethod
    def exists_resume_with_id(self, resume_id: int) -> bool:
        pass

    @abstractmethod
    def get_one_by_id(self, resume_id: int) -> Resume:
        pass

    @abstractmethod
    def get_resumes(self, filters: Iterable[IResumesFilter], searcher: ResumesSearcherBase) -> QuerySet[Resume]:
        pass

    @abstractmethod
    def get_resume_for_update(self, resume_id: int) -> Resume:
        pass

    @abstractmethod
    def get_resume_with_only_published_at(self, resume_id: int) -> Resume:
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
        self, user_id: int, sorter: IWishlistSorter
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

    def is_large_size(self, document: UploadedFile) -> bool:
        return document.size > settings.MAX_FILE_SIZE_BYTES


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

    @atomic
    def publish(self, resume_id: int) -> PublishingOut:
        resume = self.resume_repo.get_resume_for_update_with_only_published_at(resume_id)

        if resume.published_at is None:
            resume.published_at = now()
            resume.save(update_fields=["published_at"])

        return PublishingOut.from_resume(resume)

    @atomic
    def unpublish(self, resume_id: int) -> None:
        resume = self.resume_repo.get_resume_for_update_with_only_published_at(resume_id)

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

    def get_resume(self, resume_id: int) -> ResumeOut:
        return ResumeOut.from_resume(self.resume_repo.get_resume_with_user_by_id(resume_id))

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
        with atomic():
            resume = self.resume_repo.get_resume_for_update(resume_id)

            resume.desired_job = extra.desired_job
            resume.desired_salary = extra.desired_salary
            resume.experience = extra.experience

            previous_resume = resume.document.name if resume.document else None
            resume.document = (
                UploadedFile(document, self._get_filename(resume, document))
                if document is not None
                else resume.document
            )

            resume.save()

            if extra.competencies:
                self.resume_competencies_repo.delete_all_competencies_from_resume(resume_id)

                competencies = set(self.competency_repo.get_existed_competencies_by_names(set(extra.competencies)))
                self.resume_competencies_repo.attach_competencies_to_resume(resume_id, competencies)

        if previous_resume is not None:
            default_storage.delete(previous_resume)

    @staticmethod
    def _get_filename(resume: Resume, document: UploadedFile) -> str:
        return f"{resume.id}_{uuid.uuid4().hex[:10]}_{document.name}"


class ResumesWishlistService(IResumesWishlistService):
    def __init__(
        self,
        favourite_resume_repo: IFavouriteResumeRepository,
        resume_repo: IResumeRepository,
        wishlist_sorter_builder: IWishlistSorterBuilder,
    ):
        self.wishlist_sorter_builder = wishlist_sorter_builder
        self.resume_repo = resume_repo
        self.favourite_resume_repo = favourite_resume_repo

    def authorize(self, auth_user: User) -> bool:
        return auth_user.permission == Permission.EMPLOYER

    def get_user_wishlist(self, auth_user: User, params: ResumesWishlistQueryParams) -> Iterable[ResumeOut]:
        sorter = self.wishlist_sorter_builder.build(params.sort_by)

        favourites = self.favourite_resume_repo.get_wishlist_with_resumes_and_resume_owners_and_competencies_by_user_id(
            auth_user.id, sorter
        )

        return (ResumeOut.from_resume(favourite.resume) for favourite in favourites)

    def exists_resume_in_wishlist(self, auth_user: User, resume_id: int) -> bool:
        return self.favourite_resume_repo.exists_resume_in_user_wishlist(auth_user.id, resume_id)

    def add_resume_to_wishlist(self, auth_user: User, resume_id: int) -> None:
        self.favourite_resume_repo.add_resume_to_wishlist(auth_user.id, resume_id)

    def delete_resume_from_wishlist(self, auth_user: User, resume_id: int) -> None:
        self.favourite_resume_repo.delete_resume_from_wishlist(auth_user.id, resume_id)

    def is_resume_published(self, resume_id: int) -> bool:
        return self.resume_repo.get_resume_with_only_published_at(resume_id).published_at is not None


class GettingResumesService(IGettingResumesService):
    def __init__(
        self,
        resume_repo: IResumeRepository,
        filters_builder: IResumesFiltersBuilder,
        searcher_builder: IResumesSearcherBuilder,
    ):
        self.searcher_builder = searcher_builder
        self.filters_builder = filters_builder
        self.resume_repo = resume_repo

    def authorize(self, auth_user: User) -> bool:
        return auth_user.permission == Permission.EMPLOYER

    def get_resumes(self, params: ResumesQueryParams) -> ResumesOut:
        offset, limit = params.offset, params.limit

        filters = self.filters_builder.build(params)
        searcher = self.searcher_builder.build(params)

        resumes = self.resume_repo.get_resumes(filters, searcher)

        return ResumesOut.from_resumes_with_pagination(resumes, limit, offset)
