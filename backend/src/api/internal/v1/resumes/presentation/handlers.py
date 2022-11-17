from abc import ABC, abstractmethod
from typing import Iterable, Optional

from django.http import HttpRequest
from loguru import logger
from ninja import File, Form, Path, Query, UploadedFile

from api.internal.errors import ForbiddenError, NotFoundError
from api.internal.responses import SuccessResponse
from api.internal.v1.resumes.domain.entities import (
    NewResumeIn,
    PublishingOut,
    ResumeIn,
    ResumeOut,
    ResumesOut,
    ResumesQueryParams,
    ResumesWishlistQueryParams,
)
from api.internal.v1.resumes.presentation.errors import (
    AttachedDocumentIsLargeError,
    AttachedDocumentIsNotPDFError,
    ResumeAlreadyAddedToWishlistError,
    ResumeIsCreatedByUserError,
    UnpublishedResumeCannotBeAddedToWishlistError,
)
from api.internal.v1.resumes.presentation.routers import IResumeHandlers, IResumesHandlers, IResumesWishlistHandlers
from api.models import User


class ICreatingResumeService(ABC):
    @abstractmethod
    def authorize(self, auth_user: User, extra: NewResumeIn) -> bool:
        pass

    @abstractmethod
    def is_resume_created_by_user(self, extra: NewResumeIn) -> bool:
        pass

    @abstractmethod
    def create(self, extra: NewResumeIn, document: UploadedFile) -> None:
        pass


class IPublishingResumeService(ABC):
    @abstractmethod
    def authorize(self, auth_user: User, resume_id: int) -> bool:
        pass

    @abstractmethod
    def publish(self, resume_id: int) -> PublishingOut:
        pass

    @abstractmethod
    def unpublish(self, resume_id: int) -> None:
        pass


class IGettingResumeService(ABC):
    @abstractmethod
    def authorize(self, auth_user: User, resume_id: int) -> bool:
        pass

    @abstractmethod
    def get_resume(self, resume_id: int) -> ResumeOut:
        pass

    @abstractmethod
    def exists_resume_with_id(self, resume_id: int) -> bool:
        pass


class IGettingResumesService(ABC):
    @abstractmethod
    def authorize(self, auth_user: User) -> bool:
        pass

    @abstractmethod
    def get_resumes(self, params: ResumesQueryParams) -> ResumesOut:
        pass


class IUpdatingResumeService(ABC):
    @abstractmethod
    def authorize(self, auth_user: User, resume_id: int) -> bool:
        pass

    @abstractmethod
    def update(self, resume_id: int, extra: ResumeIn, document: Optional[UploadedFile]) -> None:
        pass


class IDocumentService(ABC):
    @abstractmethod
    def is_pdf(self, document: UploadedFile) -> bool:
        pass

    @abstractmethod
    def is_large_size(self, document: UploadedFile) -> bool:
        pass


class IResumesWishlistService(ABC):
    @abstractmethod
    def authorize(self, auth_user: User) -> bool:
        pass

    @abstractmethod
    def get_user_wishlist(self, auth_user: User, params: ResumesWishlistQueryParams) -> Iterable[ResumeOut]:
        pass

    @abstractmethod
    def exists_resume_in_wishlist(self, auth_user: User, resume_id: int) -> bool:
        pass

    @abstractmethod
    def add_resume_to_wishlist(self, auth_user: User, resume_id: int) -> None:
        pass

    @abstractmethod
    def delete_resume_from_wishlist(self, auth_user: User, resume_id: int) -> None:
        pass

    @abstractmethod
    def is_resume_published(self, resume_id: int) -> bool:
        pass


class ResumesHandlers(IResumesHandlers):
    def __init__(self, getting_resumes_service: IGettingResumesService):
        self.getting_resumes_service = getting_resumes_service

    def get_resumes(self, request: HttpRequest, params: ResumesQueryParams = Query(...)) -> ResumesOut:
        if not self.getting_resumes_service.authorize(request.user):
            raise ForbiddenError()

        return self.getting_resumes_service.get_resumes(params)


class ResumeHandlers(IResumeHandlers):
    def __init__(
        self,
        creating_resume_service: ICreatingResumeService,
        publishing_resume_service: IPublishingResumeService,
        getting_resume_service: IGettingResumeService,
        updating_resume_service: IUpdatingResumeService,
        document_service: IDocumentService,
    ):
        self.document_service = document_service
        self.updating_resume_service = updating_resume_service
        self.getting_resume_service = getting_resume_service
        self.publishing_resume_service = publishing_resume_service
        self.creating_resume_service = creating_resume_service

    def get_resume(self, request: HttpRequest, resume_id: int = Path(...)) -> ResumeOut:
        if not self.getting_resume_service.exists_resume_with_id(resume_id):
            raise NotFoundError()

        if not self.getting_resume_service.authorize(request.user, resume_id):
            raise ForbiddenError()

        return self.getting_resume_service.get_resume(resume_id)

    def create_resume(
        self, request: HttpRequest, extra: NewResumeIn = Form(...), document: UploadedFile = File(...)
    ) -> SuccessResponse:
        user: User = request.user

        logger.info(
            "Creating a resume user={user} extra={extra} document={document}",
            user={
                "id": user.id,
                "has_resume": hasattr(user, "resume"),
            },
            extra=extra.dict(),
            document={"name": document.name, "content_type": document.content_type, "size": document.size},
        )

        if not self.creating_resume_service.authorize(user, extra):
            logger.success("Permission denied")
            raise ForbiddenError()

        self._validate_document(document)

        if self.creating_resume_service.is_resume_created_by_user(extra):
            logger.success("The user already created a resume")
            raise ResumeIsCreatedByUserError()

        self.creating_resume_service.create(extra, document)
        logger.success("Resume was created")

        return SuccessResponse()

    def update_resume(
        self,
        request: HttpRequest,
        resume_id: int = Path(...),
        extra: ResumeIn = Form(...),
        document: UploadedFile = File(None),
    ) -> SuccessResponse:
        user: User = request.user

        logger.info(
            "Updating a resume id={resume_id} user={user} extra={extra} document={document}",
            resume_id=resume_id,
            user={
                "id": user.id,
                "resume": {"id": user.resume.id} if hasattr(user, "resume") else None,
            },
            extra=extra.dict(),
            document={"name": document.name, "content_type": document.content_type, "size": document.size}
            if document
            else None,
        )
        if not self.getting_resume_service.exists_resume_with_id(resume_id):
            logger.success("Not found the resume")
            raise NotFoundError()

        if document is not None:
            self._validate_document(document)

        if not self.updating_resume_service.authorize(user, resume_id):
            logger.success("Permission denied")
            raise ForbiddenError()

        self.updating_resume_service.update(resume_id, extra, document)
        logger.success("The resume was updated")

        return SuccessResponse()

    def publish_resume(self, request: HttpRequest, resume_id: int = Path(...)) -> PublishingOut:
        user: User = request.user

        logger.info(
            "Publishing a resume id={resume_id} user={user}",
            resume_id=resume_id,
            user={
                "id": user.id,
                "resume": {"id": user.resume.id, "published_at": user.resume.published_at}
                if hasattr(user, "resume")
                else None,
            },
        )

        if not self.getting_resume_service.exists_resume_with_id(resume_id):
            logger.success("Not found the resume")
            raise NotFoundError()

        if not self.publishing_resume_service.authorize(user, resume_id):
            logger.success("Permission denied")
            raise ForbiddenError()

        publishing_out = self.publishing_resume_service.publish(resume_id)
        logger.success("The resume was published")

        return publishing_out

    def unpublish_resume(self, request: HttpRequest, resume_id: int = Path(...)) -> SuccessResponse:
        user: User = request.user

        logger.info(
            "Unpublishing a resume id={resume_id} user={user}",
            resume_id=resume_id,
            user={
                "id": user.id,
                "resume": {"id": user.resume.id, "published_at": user.resume.published_at}
                if hasattr(user, "resume")
                else None,
            },
        )

        if not self.getting_resume_service.exists_resume_with_id(resume_id):
            logger.success("Not found the resume")
            raise NotFoundError()

        if not self.publishing_resume_service.authorize(user, resume_id):
            logger.success("Permission denied")
            raise ForbiddenError()

        self.publishing_resume_service.unpublish(resume_id)
        logger.success("The resume was unpublished")

        return SuccessResponse()

    def _validate_document(self, resume: UploadedFile) -> None:
        if not self.document_service.is_pdf(resume):
            logger.success("The attached document is not pdf")
            raise AttachedDocumentIsNotPDFError()

        if self.document_service.is_large_size(resume):
            logger.success("Size of the attached file is large")
            raise AttachedDocumentIsLargeError()


class ResumesWishlistHandlers(IResumesWishlistHandlers):
    def __init__(
        self, resumes_wishlist_service: IResumesWishlistService, getting_resume_service: IGettingResumeService
    ):
        self.getting_resume_service = getting_resume_service
        self.resumes_wishlist_service = resumes_wishlist_service

    def get_resumes_wishlist(
        self, request: HttpRequest, params: ResumesWishlistQueryParams = Query(...)
    ) -> Iterable[ResumeOut]:
        if not self.resumes_wishlist_service.authorize(request.user):
            raise ForbiddenError()

        return self.resumes_wishlist_service.get_user_wishlist(request.user, params)

    def add_resume_to_wishlist(self, request: HttpRequest, resume_id: int = Path(...)) -> SuccessResponse:
        user: User = request.user

        logger.info(
            "Adding a resume to wishlist id={resume_id} user={user}",
            resume_id=resume_id,
            user={"id": user.id, "permission": user.permission},
        )

        if not self.getting_resume_service.exists_resume_with_id(resume_id):
            logger.success("Not found the resume")
            raise NotFoundError()

        if not self.resumes_wishlist_service.authorize(user):
            logger.success("Permission denied")
            raise ForbiddenError()

        if not self.resumes_wishlist_service.is_resume_published(resume_id):
            logger.success("The resume is unpublished")
            raise UnpublishedResumeCannotBeAddedToWishlistError()

        if self.resumes_wishlist_service.exists_resume_in_wishlist(user, resume_id):
            logger.success("The resume already is in wishlist")
            raise ResumeAlreadyAddedToWishlistError()

        self.resumes_wishlist_service.add_resume_to_wishlist(user, resume_id)
        logger.success("The resume was added to wishlist")

        return SuccessResponse()

    def delete_resume_from_wishlist(self, request: HttpRequest, resume_id: int = Path(...)) -> SuccessResponse:
        user: User = request.user

        logger.info(
            "Deleting a resume from wishlist id={resume_id} user={user}",
            resume_id=resume_id,
            user={"id": user.id, "permission": user.permission},
        )

        if not self.resumes_wishlist_service.authorize(user):
            logger.success("Permission denied")
            raise ForbiddenError()

        if not self.resumes_wishlist_service.exists_resume_in_wishlist(user, resume_id):
            logger.success("Not found the resume")
            raise NotFoundError()

        self.resumes_wishlist_service.delete_resume_from_wishlist(user, resume_id)
        logger.success("The resume was deleted from wishlist")

        return SuccessResponse()
