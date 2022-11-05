from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from django.utils.timezone import now

from api.internal.v1.vacancies.domain.entities import (
    DepartmentLeaderOut,
    PublishingOut,
    VacancyDepartmentOut,
    VacancyIn,
    VacancyOut,
)
from api.internal.v1.vacancies.presentation.handlers import (
    ICreatingVacancyService,
    IGettingService,
    IPublishingVacancyService,
)
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

    @abstractmethod
    def try_get_vacancy_by_id(self, vacancy_id: int) -> Optional[Vacancy]:
        pass

    @abstractmethod
    def exists_vacancy_by_id(self, vacancy_id: int) -> bool:
        pass

    @abstractmethod
    def is_vacancy_owned(self, vacancy_id: int, employer_id: int) -> bool:
        pass

    @abstractmethod
    def set_published_at_to_vacancy_by_id(self, vacancy_id: int, published_at: datetime) -> None:
        pass

    @abstractmethod
    def get_only_published_at_by_id(self, vacancy_id: int) -> Vacancy:
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


class GettingService(IGettingService):
    def __init__(self, vacancy_repo: IVacancyRepository):
        self.vacancy_repo = vacancy_repo

    def try_get_vacancy_out_by_id(self, vacancy_id: int) -> Optional[VacancyOut]:
        vacancy = self.vacancy_repo.try_get_vacancy_by_id(vacancy_id)

        if not vacancy:
            return None

        department = vacancy.department
        leader = department.leader

        return VacancyOut(
            id=vacancy.id,
            name=vacancy.name,
            description=vacancy.description,
            expected_experience=vacancy.expected_experience,
            salary_from=vacancy.salary_from,
            salary_to=vacancy.salary_to,
            department=VacancyDepartmentOut(
                id=department.id,
                name=department.name,
                leader=DepartmentLeaderOut(
                    id=leader.id, surname=leader.surname, name=leader.name, patronymic=leader.patronymic
                ),
            ),
            published_at=vacancy.published_at,
        )

    def exists_vacancy_by_id(self, vacancy_id: int) -> bool:
        return self.vacancy_repo.exists_vacancy_by_id(vacancy_id)


class PublishingVacancyService(IPublishingVacancyService):
    def __init__(self, vacancy_repo: IVacancyRepository):
        self.vacancy_repo = vacancy_repo

    def authorize(self, auth_user: User, vacancy_id: int) -> bool:
        is_employer = auth_user.permission == Permission.EMPLOYER
        is_leader = hasattr(auth_user, "department") and self.vacancy_repo.is_vacancy_owned(vacancy_id, auth_user.id)

        return is_employer and is_leader

    def publish(self, vacancy_id: int) -> PublishingOut:
        vacancy = self.vacancy_repo.get_only_published_at_by_id(vacancy_id)
        published_at = vacancy.published_at or now()

        self.vacancy_repo.set_published_at_to_vacancy_by_id(vacancy_id, published_at)

        return PublishingOut(published_at=published_at)
