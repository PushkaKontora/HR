from abc import ABC, abstractmethod
from typing import Optional

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from ninja import UploadedFile

from api.internal.v1.vacancy_requests.domain.entities import RequestIn
from api.models import User, VacancyRequest


class IVacancyRequestNotifier(ABC):
    @abstractmethod
    def notify(
        self,
        request: VacancyRequest,
        sender: User,
        employer: User,
        data: RequestIn,
        resume: Optional[UploadedFile],
    ) -> None:
        pass


class EmailNotifier(IVacancyRequestNotifier):
    TEMPLATE_NAME = "vacancy_request.html"
    RESUME_FILENAME = "resume.pdf"

    def notify(
        self,
        request: VacancyRequest,
        sender: User,
        employer: User,
        data: RequestIn,
        resume: Optional[UploadedFile],
    ) -> None:
        context = {
            "request_id": request.id,
            "sender": {
                "id": sender.id,
                "surname": sender.surname,
                "name": sender.name,
                "patronymic": sender.patronymic,
                "email": sender.email,
            },
            "employer": {
                "id": employer.id,
                "surname": employer.surname,
                "name": employer.name,
                "patronymic": employer.patronymic,
            },
            "vacancy": {"id": request.vacancy.id, "name": request.vacancy.name},
        }
        html = render_to_string(self.TEMPLATE_NAME, context)

        email = EmailMultiAlternatives(
            subject=settings.VACANCY_REQUEST_EMAIL_SUBJECT,
            from_email=settings.SUPPORT_EMAIL_ADDRESS,
            to=[employer.email],
        )
        email.attach_alternative(html, "text/html")

        if resume:
            resume.seek(0)
            email.attach(self.RESUME_FILENAME, resume.read(), "application/pdf")

        email.send()
