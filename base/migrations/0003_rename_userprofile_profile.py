# Generated by Django 5.2.1 on 2025-05-26 15:07

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0002_userprofile_delete_profile"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="UserProfile",
            new_name="Profile",
        ),
    ]
