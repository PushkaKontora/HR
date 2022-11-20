from abc import ABC, abstractmethod
from typing import Iterable, Optional

from django.http import HttpRequest
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
from api.logging import get_logger
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
        auth_user: User = request.user
        logger = get_logger(request)

        logger.info(
            "Creating a resume auth_user={auth_user} extra={extra} document={document}".format(
                auth_user={
                    "id": auth_user.id,
                    "has_resume": hasattr(auth_user, "resume"),
                },
                extra=extra.dict(),
                document={"name": document.name, "content_type": document.content_type, "size": document.size},
            ),
        )

        logger.info("Authorization...")
        if not self.creating_resume_service.authorize(auth_user, extra):
            logger.success("Permission denied")
            raise ForbiddenError()

        self._validate_document(request, document)

        logger.info("Checking an existence of the user resume...")
        if self.creating_resume_service.is_resume_created_by_user(extra):
            logger.success("The user already created a resume")
            raise ResumeIsCreatedByUserError()

        logger.info("Creating a resume...")
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
        auth_user: User = request.user
        logger = get_logger(request)

        logger.info(
            "Updating a resume id={resume_id} auth_user={auth_user} extra={extra} document={document}".format(
                resume_id=resume_id,
                auth_user={
                    "id": auth_user.id,
                    "resume": {"id": auth_user.resume.id} if hasattr(auth_user, "resume") else None,
                },
                extra=extra.dict(),
                document={"name": document.name, "content_type": document.content_type, "size": document.size}
                if document
                else None,
            )
        )

        logger.info("Checking an existence of the resume...")
        if not self.getting_resume_service.exists_resume_with_id(resume_id):
            logger.success("Not found the resume")
            raise NotFoundError()

        if document is not None:
            self._validate_document(request, document)

        logger.info("Authorization...")
        if not self.updating_resume_service.authorize(auth_user, resume_id):
            logger.success("Permission denied")
            raise ForbiddenError()

        logger.info("Updating the resume...")
        self.updating_resume_service.update(resume_id, extra, document)
        logger.success("The resume was updated")

        return SuccessResponse()

    def publish_resume(self, request: HttpRequest, resume_id: int = Path(...)) -> PublishingOut:
        if not self.getting_resume_service.exists_resume_with_id(resume_id):
            raise NotFoundError()

        if not self.publishing_resume_service.authorize(request.user, resume_id):
            raise ForbiddenError()

        return self.publishing_resume_service.publish(resume_id)

    def unpublish_resume(self, request: HttpRequest, resume_id: int = Path(...)) -> SuccessResponse:
        if not self.getting_resume_service.exists_resume_with_id(resume_id):
            raise NotFoundError()

        if not self.publishing_resume_service.authorize(request.user, resume_id):
            raise ForbiddenError()

        self.publishing_resume_service.unpublish(resume_id)

        return SuccessResponse()

    def _validate_document(self, request: HttpRequest, resume: UploadedFile) -> None:
        logger = get_logger(request)
        logger.info("Checking the resume file...")

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
        if not self.getting_resume_service.exists_resume_with_id(resume_id):
            raise NotFoundError()

        if not self.resumes_wishlist_service.authorize(request.user):
            raise ForbiddenError()

        if not self.resumes_wishlist_service.is_resume_published(resume_id):
            raise UnpublishedResumeCannotBeAddedToWishlistError()

        if self.resumes_wishlist_service.exists_resume_in_wishlist(request.user, resume_id):
            raise ResumeAlreadyAddedToWishlistError()

        self.resumes_wishlist_service.add_resume_to_wishlist(request.user, resume_id)

        return SuccessResponse()

    def delete_resume_from_wishlist(self, request: HttpRequest, resume_id: int = Path(...)) -> SuccessResponse:
        if not self.resumes_wishlist_service.authorize(request.user):
            raise ForbiddenError()

        if not self.resumes_wishlist_service.exists_resume_in_wishlist(request.user, resume_id):
            raise NotFoundError()

        self.resumes_wishlist_service.delete_resume_from_wishlist(request.user, resume_id)

        return SuccessResponse()
