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


class DepartmentRepository(IDepartmentRepository):
    def exists_department_with_id(self, department_id: int) -> bool:
        return Department.objects.filter(id=department_id).exists()
