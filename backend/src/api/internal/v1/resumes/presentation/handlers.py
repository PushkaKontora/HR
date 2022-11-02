from abc import ABC, abstractmethod
from typing import Iterable, Optional

from django.http import HttpRequest
from ninja import Body, File, Form, Path, Query, UploadedFile
from ninja.pagination import LimitOffsetPagination, paginate

from api.internal.v1.exceptions import ForbiddenError, NotFoundError
from api.internal.v1.responses import SuccessResponse
from api.internal.v1.resumes.domain.entities import (
    NewResumeIn,
    PublishingOut,
    ResumeIn,
    ResumeOut,
    ResumesFilters,
    ResumesWishlistFilters,
    ResumesWishlistIn,
)
from api.internal.v1.resumes.presentation.exceptions import AttachedDocumentIsNotPDFError, ResumeIsCreatedByUserError
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


class ResumesHandlers(IResumesHandlers):
    @paginate(LimitOffsetPagination)
    def get_resumes(self, request: HttpRequest, filters: ResumesFilters = Query(...)) -> Iterable[ResumeOut]:
        raise NotImplementedError()


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
    def get_resumes_wishlist(
        self, request: HttpRequest, filters: ResumesWishlistFilters = Query(...)
    ) -> Iterable[ResumeOut]:
        raise NotImplementedError()

    def add_resume_to_wishlist(self, request: HttpRequest, body: ResumesWishlistIn = Body(...)) -> SuccessResponse:
        raise NotImplementedError()
