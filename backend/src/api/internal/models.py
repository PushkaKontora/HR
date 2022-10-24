from django.db import models


class Permissions(models.TextChoices):
    USER = "user"
    EMPLOYER = "employer"
    ADMIN = "admin"


class Experiences(models.TextChoices):
    NO_EXPERIENCE = "no_experience"
    FROM_ONE_TO_THREE_YEARS = "from_one_to_three_years"
    FROM_THREE_TO_SIX_YEARS = "from_three_to_six_years"
    MORE_THAN_SIX_YEARS = "more_than_six_years"


class User:
    pass
