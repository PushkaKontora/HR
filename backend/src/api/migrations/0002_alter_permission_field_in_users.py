# Generated by Django 4.1.2 on 2022-10-27 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_init"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="permission",
            field=models.CharField(
                choices=[("user", "User"), ("employer", "Employer"), ("admin", "Admin")], default="user", max_length=32
            ),
        ),
    ]
