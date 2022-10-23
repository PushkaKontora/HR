from ninja import NinjaAPI

from api.internal.v1.departments.api import register_departments_api
from api.internal.v1.users.api import register_users_api

apis_registrations = [register_users_api, register_departments_api]


def get_api() -> NinjaAPI:
    base = NinjaAPI(title="HR")

    for register in apis_registrations:
        register(base)

    return base
