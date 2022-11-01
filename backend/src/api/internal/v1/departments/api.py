from dependency_injector import containers, providers
from ninja import NinjaAPI

from api.internal.v1.departments.db.repositories import DepartmentRepository
from api.internal.v1.departments.domain.services import GettingService
from api.internal.v1.departments.presentation.handlers import DepartmentHandlers, DepartmentsHandlers
from api.internal.v1.departments.presentation.routers import DepartmentRouter, DepartmentsRouter


class DepartmentsContainer(containers.DeclarativeContainer):
    department_repo = providers.Singleton(DepartmentRepository)

    getting_service = providers.Singleton(GettingService, department_repo=department_repo)

    department_handlers = providers.Singleton(DepartmentHandlers, getting_service=getting_service)
    departments_handlers = providers.Singleton(DepartmentsHandlers, getting_service=getting_service)

    department_router = providers.Singleton(DepartmentRouter, department_handlers=department_handlers)
    departments_router = providers.Singleton(
        DepartmentsRouter, department_router=department_router, departments_handlers=departments_handlers
    )


def register_departments_api(base: NinjaAPI) -> None:
    container = DepartmentsContainer()

    base.add_router("/departments", container.departments_router())
