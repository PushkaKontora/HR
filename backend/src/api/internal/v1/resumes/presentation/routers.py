from abc import ABC, abstractmethod
from typing import Iterable, List, Optional

from django.conf import settings
from django.http import HttpRequest
from ninja import File, Form, Path, Query, Router, UploadedFile
from ninja.security import HttpBearer

from api.internal.responses import DomainErrorResponse, MessageResponse, SuccessResponse
from api.internal.v1.resumes.domain.entities import (
    NewResumeIn,
    PublishingOut,
    ResumeOut,
    ResumesOut,
    ResumesQueryParams,
    ResumesWishlistQueryParams,
)

RESUMES_TAG = "resumes"


class IResumesHandlers(ABC):
    @abstractmethod
    def get_resumes(self, request: HttpRequest, params: ResumesQueryParams = Query(...)) -> ResumesOut:
        pass


class IResumeHandlers(ABC):
    @abstractmethod
    def get_resume(self, request: HttpRequest, resume_id: int = Path(...)) -> ResumeOut:
        pass

    @abstractmethod
    def create_resume(
        self, request: HttpRequest, extra: NewResumeIn = Form(...), document: Optional[UploadedFile] = File(None)
    ) -> SuccessResponse:
        pass

    @abstractmethod
    def update_partial_resume(
        self,
        request: HttpRequest,
        resume_id: int = Path(...),
        extra: NewResumeIn = Form(...),
        document: Optional[UploadedFile] = File(None),
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
        self, request: HttpRequest, filters: ResumesWishlistQueryParams = Query(...)
    ) -> Iterable[ResumeOut]:
        pass

    @abstractmethod
    def add_resume_to_wishlist(self, request: HttpRequest, resume_id: int = Path(...)) -> SuccessResponse:
        pass

    @abstractmethod
    def delete_resume_from_wishlist(self, request: HttpRequest, resume_id: int = Path(...)) -> SuccessResponse:
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
            path="",
            methods=["GET"],
            view_func=resumes_handlers.get_resumes,
            auth=[auth],
            response={200: ResumesOut},
        )

        self.add_api_operation(
            path="",
            methods=["POST"],
            view_func=resume_handlers.create_resume,
            auth=[auth],
            response={200: SuccessResponse, 401: MessageResponse, 403: MessageResponse, 422: DomainErrorResponse},
            description=f"""
    422 error codes:
        1 - the user already created a resume
        2 - the attached document is not a pdf file
        5 - the attached document size must be lte than {settings.MAX_FILE_SIZE_BYTES} bytes
    """,
        )

        self.add_router("/wishlist", resumes_wishlist_router)
        self.add_router("/{int:resume_id}", resume_router)


class ResumeRouter(Router):
    def __init__(self, resume_handlers: IResumeHandlers, auth: HttpBearer):
        super(ResumeRouter, self).__init__(tags=[RESUMES_TAG])

        self.add_api_operation(
            path="",
            methods=["GET"],
            auth=[auth],
            view_func=resume_handlers.get_resume,
            response={200: ResumeOut, 403: MessageResponse, 404: MessageResponse},
        )

        self.add_api_operation(
            path="",
            methods=["POST"],
            auth=[auth],
            view_func=resume_handlers.update_partial_resume,
            response={
                200: SuccessResponse,
                401: MessageResponse,
                403: MessageResponse,
                404: MessageResponse,
                422: MessageResponse,
            },
            description=f"""
    422 error codes:
        2 - the attached document is not a pdf file
        5 - the attached document size must be lte than {settings.MAX_FILE_SIZE_BYTES} bytes"
    """,
        )

        self.add_api_operation(
            path="/publish",
            methods=["PATCH"],
            auth=[auth],
            view_func=resume_handlers.publish_resume,
            response={200: PublishingOut, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
            description="""
    422 error codes:
        6 - Desired job and document must be set before publishing
    """,
        )

        self.add_api_operation(
            path="/unpublish",
            methods=["PATCH"],
            auth=[auth],
            view_func=resume_handlers.unpublish_resume,
            response={200: SuccessResponse, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
        )


class ResumesWishlistRouter(Router):
    def __init__(self, resumes_wishlist_handlers: IResumesWishlistHandlers, auth: HttpBearer):
        super(ResumesWishlistRouter, self).__init__(tags=[RESUMES_TAG], auth=[auth])

        self.add_api_operation(
            path="",
            methods=["GET"],
            view_func=resumes_wishlist_handlers.get_resumes_wishlist,
            response={200: List[ResumeOut], 401: MessageResponse, 403: MessageResponse},
        )

        self.add_api_operation(
            path="/{int:resume_id}",
            methods=["POST"],
            view_func=resumes_wishlist_handlers.add_resume_to_wishlist,
            response={200: SuccessResponse, 401: MessageResponse, 403: MessageResponse, 422: MessageResponse},
            description="""
    422 error codes:
        3 - the resume already added to wishlist
        4 - you cannot add an unpublished resume to wishlist
    """,
        )

        self.add_api_operation(
            path="/{int:resume_id}",
            methods=["DELETE"],
            view_func=resumes_wishlist_handlers.delete_resume_from_wishlist,
            response={200: SuccessResponse, 401: MessageResponse, 403: MessageResponse, 404: MessageResponse},
        )
