from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
from requests import get

from api.models import Experience

Vacancy = apps.get_model("api", "Vacancy")
Department = apps.get_model("api", "Department")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not settings.DEBUG:
            raise ValueError("Only debug mode")

        if not (department := Department.objects.first()):
            raise ObjectDoesNotExist("Not found any department")

        vacancies = []
        for i in range(10):
            response = get(f"https://api.hh.ru/vacancies?per_page=100&page={i}")

            for item in response.json()["items"]:
                if "salary" not in item or item["salary"] is None:
                    continue

                salary = item["salary"]
                vacancies.append(
                    Vacancy(
                        name=item["name"],
                        department=department,
                        salary_from=salary["from"],
                        salary_to=salary["to"],
                        published_at=item.get("published_at"),
                        expected_experience=Experience.NO_EXPERIENCE,
                    )
                )

        Vacancy.objects.bulk_create(vacancies)
