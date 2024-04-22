# Generated by Django 5.0.4 on 2024-04-15 04:45

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("corecode", "0004_auto_20201124_0614"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "staff_type",
                    models.CharField(
                        choices=[
                            ("admin", "Admin"),
                            ("teacher", "Teacher"),
                            ("finance", "Finance"),
                        ],
                        default="admin",
                        max_length=10,
                    ),
                ),
                (
                    "current_status",
                    models.CharField(
                        choices=[("active", "Active"), ("inactive", "Inactive")],
                        default="active",
                        max_length=10,
                    ),
                ),
                ("surname", models.CharField(max_length=200)),
                ("firstname", models.CharField(max_length=200)),
                ("other_name", models.CharField(blank=True, max_length=200)),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "Male"), ("female", "Female")],
                        default="male",
                        max_length=10,
                    ),
                ),
                ("date_of_birth", models.DateField(default=django.utils.timezone.now)),
                (
                    "date_of_admission",
                    models.DateField(default=django.utils.timezone.now),
                ),
                (
                    "mobile_number",
                    models.CharField(
                        blank=True,
                        max_length=13,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Entered mobile number isn't in a right format!",
                                regex="^[0-9]{10,15}$",
                            )
                        ],
                    ),
                ),
                ("address", models.TextField(blank=True)),
                ("others", models.TextField(blank=True)),
                (
                    "subject",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="corecode.subject",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]