from typing import Iterable

from django.http import HttpRequest
from ninja import Body, File, Form, Path, Query, UploadedFile

from api.internal.base import SuccessResponse
from api.internal.v1.resumes.domain.entities import (
    PublishingOut,
    ResumeFormIn,
    ResumeOut,
    ResumesFilters,
    ResumesWishlistFilters,
    ResumesWishlistIn,
)
from api.internal.v1.resumes.presentation.routers import IResumeHandlers, IResumesHandlers, IResumesWishlistHandlers


class ResumesHandlers(IResumesHandlers):
    def get_resumes(self, request: HttpRequest, filters: ResumesFilters = Query(...)) -> Iterable[ResumeOut]:
        pass


class ResumeHandlers(IResumeHandlers):
    def get_resume(self, request: HttpRequest, resume_id: int = Path(...)) -> ResumeOut:
        pass

    def create_resume(
        self, request: HttpRequest, extra: ResumeFormIn = Form(...), document: UploadedFile = File(...)
    ) -> SuccessResponse:
        pass

    def update_resume(
        self,
        request: HttpRequest,
        resume_id: int = Path(...),
        extra: ResumeFormIn = Form(...),
        document: UploadedFile = File(...),
    ) -> SuccessResponse:
        pass

    def publish_resume(self, request: HttpRequest, resume_id: int = Path(...)) -> PublishingOut:
        pass

    def unpublish_resume(self, request: HttpRequest, resume_id: int = Path(...)) -> SuccessResponse:
        pass


class ResumesWishlistHandlers(IResumesWishlistHandlers):
    def get_resumes_wishlist(
        self, request: HttpRequest, filters: ResumesWishlistFilters = Query(...)
    ) -> Iterable[ResumeOut]:
        pass

    def add_resume_to_wishlist(self, request: HttpRequest, body: ResumesWishlistIn = Body(...)) -> SuccessResponse:
        pass