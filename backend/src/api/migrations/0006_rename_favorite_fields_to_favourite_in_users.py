# Generated by Django 4.1.2 on 2022-11-04 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_change_names_of_many_tables"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="favorite_resumes",
            new_name="favourite_resumes",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="favorite_vacancies",
            new_name="favourite_vacancies",
        ),
    ]
