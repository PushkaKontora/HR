from abc import ABC, abstractmethod
from typing import Iterable, Optional

from django.http import HttpRequest
from ninja import File, Form, Path, Query, UploadedFile

from api.internal.v1.errors import ForbiddenError, NotFoundError
from api.internal.v1.responses import SuccessResponse
from api.internal.v1.resumes.domain.entities import (
    NewResumeIn,
    PublishingOut,
    ResumeIn,
    ResumeOut,
    ResumesOut,
    ResumesParams,
    ResumesWishlistParameters,
)
from api.internal.v1.resumes.presentation.errors import (
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
    def get_resume_out(self, resume_id: int) -> ResumeOut:
        pass

    @abstractmethod
    def exists_resume_with_id(self, resume_id: int) -> bool:
        pass


class IGettingResumesService(ABC):
    @abstractmethod
    def authorize(self, auth_user: User) -> bool:
        pass

    @abstractmethod
    def get_resumes_out(self, params: ResumesParams) -> ResumesOut:
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


class IResumesWishlistService(ABC):
    @abstractmethod
    def authorize(self, auth_user: User) -> bool:
        pass

    @abstractmethod
    def get_user_wishlist(self, auth_user: User, params: ResumesWishlistParameters) -> Iterable[ResumeOut]:
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

    def get_resumes(self, request: HttpRequest, params: ResumesParams = Query(...)) -> ResumesOut:
        if not self.getting_resumes_service.authorize(request.user):
            raise ForbiddenError()

        return self.getting_resumes_service.get_resumes_out(params)


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

        return self.getting_resume_service.get_resume_out(resume_id)

    def create_resume(
        self, request: HttpRequest, extra: NewResumeIn = Form(...), document: UploadedFile = File(...)
    ) -> SuccessResponse:
        if not self.document_service.is_pdf(document):
            raise AttachedDocumentIsNotPDFError()

        if not self.creating_resume_service.authorize(request.user, extra):
            raise ForbiddenError()

        if self.creating_resume_service.is_resume_created_by_user(extra):
            raise ResumeIsCreatedByUserError()

        self.creating_resume_service.create(extra, document)

        return SuccessResponse()

    def update_resume(
        self,
        request: HttpRequest,
        resume_id: int = Path(...),
        extra: ResumeIn = Form(...),
        document: UploadedFile = File(None),
    ) -> SuccessResponse:
        if not self.getting_resume_service.exists_resume_with_id(resume_id):
            raise NotFoundError()

        if document is not None and not self.document_service.is_pdf(document):
            raise AttachedDocumentIsNotPDFError()

        if not self.updating_resume_service.authorize(request.user, resume_id):
            raise ForbiddenError()

        self.updating_resume_service.update(resume_id, extra, document)

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


class ResumesWishlistHandlers(IResumesWishlistHandlers):
    def __init__(
        self, resumes_wishlist_service: IResumesWishlistService, getting_resume_service: IGettingResumeService
    ):
        self.getting_resume_service = getting_resume_service
        self.resumes_wishlist_service = resumes_wishlist_service

    def get_resumes_wishlist(
        self, request: HttpRequest, params: ResumesWishlistParameters = Query(...)
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
