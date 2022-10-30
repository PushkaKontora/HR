from typing import Optional

from django.db.models import QuerySet

from api.internal.v1.departments.domain.services import IDepartmentRepository
from api.models import Department


class DepartmentRepository(IDepartmentRepository):
    def try_get_one_with_leader(self, department_id: int) -> Optional[Department]:
        return Department.objects.select_related("leader").filter(id=department_id).first()

    def get_all(self) -> QuerySet[Department]:
        return Department.objects.all()
