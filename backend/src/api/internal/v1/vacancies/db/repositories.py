from datetime import datetime
from typing import Optional

from api.internal.v1.vacancies.domain.services import IDepartmentRepository, IVacancyRepository
from api.models import Department, Experience, Vacancy


class VacancyRepository(IVacancyRepository):
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
        return Vacancy.objects.create(
            department_id=department_id,
            name=name,
            description=description,
            expected_experience=expected_experience,
            salary_from=salary_from,
            salary_to=salary_to,
            published_at=published_at,
        )

    def try_get_vacancy_by_id(self, vacancy_id: int) -> Optional[Vacancy]:
        return Vacancy.objects.filter(id=vacancy_id).first()

    def exists_vacancy_by_id(self, vacancy_id: int) -> bool:
        return Vacancy.objects.filter(id=vacancy_id).exists()

    def is_vacancy_owned(self, vacancy_id: int, employer_id: int) -> bool:
        return Vacancy.objects.filter(id=vacancy_id, department__leader_id=employer_id).exists()

    def set_published_at_to_vacancy_by_id(self, vacancy_id: int, published_at: datetime) -> None:
        Vacancy.objects.filter(id=vacancy_id).update(published_at=published_at)

    def get_only_published_at_by_id(self, vacancy_id: int) -> Vacancy:
        return Vacancy.objects.only("published_at").get(id=vacancy_id)


class DepartmentRepository(IDepartmentRepository):
    def exists_department_with_id(self, department_id: int) -> bool:
        return Department.objects.filter(id=department_id).exists()
