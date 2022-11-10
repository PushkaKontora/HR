from typing import Optional

from api.internal.v1.vacancy_requests.domain.services import (
    IUserRepository,
    IVacancyRepository,
    IVacancyRequestRepository,
)
from api.models import User, Vacancy, VacancyRequest


class UserRepository(IUserRepository):
    def get_employer_by_vacancy_id(self, vacancy_id: int) -> User:
        return User.objects.filter(department__vacancies=vacancy_id).get()


class VacancyRequestRepository(IVacancyRequestRepository):
    def create(self, user_id: int, vacancy_id: int) -> VacancyRequest:
        return VacancyRequest.objects.create(owner_id=user_id, vacancy_id=vacancy_id)

    def try_get_last_by_owner_id_and_vacancy_id(self, owner_id: int, vacancy_id: int) -> Optional[VacancyRequest]:
        return VacancyRequest.objects.filter(owner_id=owner_id, vacancy_id=vacancy_id).last()


class VacancyRepository(IVacancyRepository):
    def exists_vacancy_with_id(self, vacancy_id: int) -> bool:
        return Vacancy.objects.filter(id=vacancy_id).exists()
