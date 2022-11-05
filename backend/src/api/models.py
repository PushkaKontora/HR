from django.contrib.postgres.indexes import GinIndex
from django.db import models


class Permission(models.TextChoices):
    USER = "user"
    EMPLOYER = "employer"
    ADMIN = "admin"


class Experience(models.TextChoices):
    NO_EXPERIENCE = "no_experience"
    FROM_ONE_TO_THREE_YEARS = "from_one_to_three_years"
    FROM_THREE_TO_SIX_YEARS = "from_three_to_six_years"
    MORE_THAN_SIX_YEARS = "more_than_six_years"


class User(models.Model):
    email = models.EmailField(max_length=256, unique=True)
    permission = models.CharField(max_length=32, choices=Permission.choices, default=Permission.USER)
    surname = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    patronymic = models.CharField(max_length=128)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True)
    favourite_vacancies = models.ManyToManyField("Vacancy", through="FavouriteVacancy")
    favourite_resumes = models.ManyToManyField("Resume", through="FavouriteResume")

    class Meta:
        db_table = "users"


class Password(models.Model):
    owner = models.OneToOneField("User", on_delete=models.CASCADE, related_name="password")
    value = models.CharField(max_length=512)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "passwords"


class Resume(models.Model):
    owner = models.OneToOneField("User", on_delete=models.CASCADE, related_name="resume")
    document = models.FileField(upload_to="resumes/%Y/%m/%d/")
    desired_job = models.CharField(max_length=128)
    experience = models.CharField(max_length=32, choices=Experience.choices, null=True)
    desired_salary = models.PositiveIntegerField(null=True)
    competencies = models.ManyToManyField("Competency", through="ResumeCompetency")
    published_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "resumes"
        indexes = [GinIndex(name="desired_job_idx", fields=["desired_job"], opclasses=["gin_trgm_ops"])]


class ResumeCompetency(models.Model):
    resume = models.ForeignKey("Resume", on_delete=models.CASCADE)
    competency = models.ForeignKey("Competency", on_delete=models.CASCADE)

    class Meta:
        db_table = "resumes_competencies"
        unique_together = ["resume", "competency"]


class Competency(models.Model):
    name = models.CharField(primary_key=True, max_length=64)

    class Meta:
        db_table = "competencies"


class Department(models.Model):
    leader = models.OneToOneField("User", on_delete=models.PROTECT, related_name="department")
    name = models.CharField(max_length=256)
    description = models.TextField(null=True)

    class Meta:
        db_table = "departments"


class Vacancy(models.Model):
    department = models.ForeignKey("Department", on_delete=models.CASCADE, related_name="vacancies")
    name = models.CharField(max_length=256)
    description = models.TextField(null=True)
    expected_experience = models.CharField(max_length=32, choices=Experience.choices)
    salary_from = models.PositiveIntegerField(null=True)
    salary_to = models.PositiveIntegerField(null=True)
    published_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "vacancies"


class VacancyRequest(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE)
    vacancy = models.ForeignKey("Vacancy", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "vacancies_requests"


class IssuedToken(models.Model):
    value = models.CharField(primary_key=True, max_length=512)
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="issued_tokens")
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "issued_tokens"


class FavouriteVacancy(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    vacancy = models.ForeignKey("Vacancy", on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "favourite_vacancies"


class FavouriteResume(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    resume = models.ForeignKey("Resume", on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "favourite_resumes"
