# Generated by Django 5.2.1 on 2025-05-31 16:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0007_alter_employee_salary_type_alter_jobrole_keywords"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="linked_user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="employee_profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
