from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from django.utils.timezone import now

from api.internal.v1.vacancies.domain.entities import VacancyIn
from api.internal.v1.vacancies.presentation.handlers import ICreatingVacancyService
from api.models import Experience, Permission, User, Vacancy


class IVacancyRepository(ABC):
    @abstractmethod
    def create(
        self,
        department_id: int,
        name: str,
        description: str,
        expected_experience: Experience,
        salary_to: Optional[int],
        salary_from: Optional[int],
        published_at: Optional[datetime],
    ) -> Vacancy:
        pass


class IDepartmentRepository(ABC):
    @abstractmethod
    def exists_department_with_id(self, department_id: int) -> bool:
        pass


class CreatingVacancyService(ICreatingVacancyService):
    def __init__(self, vacancy_repo: IVacancyRepository, department_repo: IDepartmentRepository):
        self.department_repo = department_repo
        self.vacancy_repo = vacancy_repo

    def exists_department_with_id(self, department_id: int) -> bool:
        return self.department_repo.exists_department_with_id(department_id)

    def authorize(self, auth_user: User, body: VacancyIn) -> bool:
        is_employer = auth_user.permission == Permission.EMPLOYER
        is_leader = hasattr(auth_user, "department") and auth_user.department.id == body.department_id

        return is_employer and is_leader

    def create(self, body: VacancyIn) -> None:
        self.vacancy_repo.create(
            body.department_id,
            body.name,
            body.description,
            body.expected_experience,
            body.salary_to,
            body.salary_from,
            published_at=now() if body.published else None,
        )
