# Generated by Django 4.2.7 on 2023-12-11 08:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("projects_manager", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Comment",
        ),
        migrations.DeleteModel(
            name="Issue",
        ),
        migrations.AlterField(
            model_name="project",
            name="contributors",
            field=models.ManyToManyField(
                limit_choices_to={"is_active": True},
                related_name="contributing_projects",
                through="projects_manager.Contributor",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
