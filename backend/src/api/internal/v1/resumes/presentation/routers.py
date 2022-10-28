from abc import ABC, abstractmethod
from typing import Iterable, List

from django.http import HttpRequest
from ninja import Body, File, Form, Path, Query, Router, UploadedFile
from ninja.security import HttpBearer

from api.internal.v1.responses import ErrorResponse, SuccessResponse
from api.internal.v1.resumes.domain.entities import (
    PublishingOut,
    ResumeFormIn,
    ResumeOut,
    ResumesFilters,
    ResumesWishlistFilters,
    ResumesWishlistIn,
)
from api.internal.v1.tags import NOT_IMPLEMENTED_TAG

RESUMES_TAG = "resumes"


class IResumesHandlers(ABC):
    @abstractmethod
    def get_resumes(self, request: HttpRequest, filters: ResumesFilters = Query(...)) -> Iterable[ResumeOut]:
        pass


class IResumeHandlers(ABC):
    @abstractmethod
    def get_resume(self, request: HttpRequest, resume_id: int = Path(...)) -> ResumeOut:
        pass

    @abstractmethod
    def create_resume(
        self, request: HttpRequest, extra: ResumeFormIn = Form(...), document: UploadedFile = File(...)
    ) -> SuccessResponse:
        pass

    @abstractmethod
    def update_resume(
        self,
        request: HttpRequest,
        resume_id: int = Path(...),
        extra: ResumeFormIn = Form(...),
        document: UploadedFile = File(...),
    ) -> SuccessResponse:
        pass

    @abstractmethod
    def publish_resume(self, request: HttpRequest, resume_id: int = Path(...)) -> PublishingOut:
        pass

    @abstractmethod
    def unpublish_resume(self, request: HttpRequest, resume_id: int = Path(...)) -> SuccessResponse:
        pass


class IResumesWishlistHandlers(ABC):
    @abstractmethod
    def get_resumes_wishlist(
        self, request: HttpRequest, filters: ResumesWishlistFilters = Query(...)
    ) -> Iterable[ResumeOut]:
        pass

    @abstractmethod
    def add_resume_to_wishlist(self, request: HttpRequest, body: ResumesWishlistIn = Body(...)) -> SuccessResponse:
        pass


class ResumesRouter(Router):
    def __init__(
        self,
        resume_router: Router,
        resumes_wishlist_router: Router,
        resumes_handlers: IResumesHandlers,
        resume_handlers: IResumeHandlers,
        auth: HttpBearer,
    ):
        super(ResumesRouter, self).__init__(tags=[RESUMES_TAG])

        self.add_api_operation(
            tags=[RESUMES_TAG, NOT_IMPLEMENTED_TAG],
            path="",
            methods=["GET"],
            view_func=resumes_handlers.get_resumes,
            response={200: List[ResumeOut]},
        )

        self.add_api_operation(
            tags=[RESUMES_TAG, NOT_IMPLEMENTED_TAG],
            path="",
            methods=["POST"],
            view_func=resume_handlers.create_resume,
            auth=[auth],
            response={200: SuccessResponse, 401: ErrorResponse, 422: ErrorResponse},
        )

        self.add_router("/wishlist", resumes_wishlist_router)
        self.add_router("/{int:resume_id}", resume_router)


class ResumeRouter(Router):
    def __init__(self, resume_handlers: IResumeHandlers, auth: HttpBearer):
        super(ResumeRouter, self).__init__(tags=[RESUMES_TAG])

        self.add_api_operation(
            tags=[RESUMES_TAG, NOT_IMPLEMENTED_TAG],
            path="",
            methods=["GET"],
            view_func=resume_handlers.get_resume,
            response={200: ResumeOut, 404: ErrorResponse},
        )

        self.add_api_operation(
            tags=[RESUMES_TAG, NOT_IMPLEMENTED_TAG],
            path="",
            methods=["PUT"],
            auth=[auth],
            view_func=resume_handlers.update_resume,
            response={
                200: SuccessResponse,
                401: ErrorResponse,
                404: ErrorResponse,
                422: ErrorResponse,
            },
        )

        self.add_api_operation(
            tags=[RESUMES_TAG, NOT_IMPLEMENTED_TAG],
            path="/publish",
            methods=["PATCH"],
            auth=[auth],
            view_func=resume_handlers.publish_resume,
            response={200: PublishingOut, 401: ErrorResponse, 404: ErrorResponse},
        )

        self.add_api_operation(
            tags=[RESUMES_TAG, NOT_IMPLEMENTED_TAG],
            path="/unpublish",
            methods=["PATCH"],
            auth=[auth],
            view_func=resume_handlers.unpublish_resume,
            response={200: SuccessResponse, 401: ErrorResponse, 404: ErrorResponse},
        )


class ResumesWishlistRouter(Router):
    def __init__(self, wishlist_resumes_handlers: IResumesWishlistHandlers, auth: HttpBearer):
        super(ResumesWishlistRouter, self).__init__(tags=[RESUMES_TAG])

        self.add_api_operation(
            tags=[RESUMES_TAG, NOT_IMPLEMENTED_TAG],
            path="",
            methods=["GET"],
            auth=[auth],
            view_func=wishlist_resumes_handlers.get_resumes_wishlist,
            response={200: List[ResumeOut], 401: ErrorResponse, 403: ErrorResponse},
        )

        self.add_api_operation(
            tags=[RESUMES_TAG, NOT_IMPLEMENTED_TAG],
            path="",
            methods=["POST"],
            auth=[auth],
            view_func=wishlist_resumes_handlers.add_resume_to_wishlist,
            response={200: SuccessResponse, 401: ErrorResponse, 403: ErrorResponse, 422: ErrorResponse},
        )
