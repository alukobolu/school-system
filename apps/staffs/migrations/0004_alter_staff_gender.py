# Generated by Django 5.0.4 on 2024-04-15 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staffs", "0003_staff_staff_type_staff_subject_staff_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staff",
            name="gender",
            field=models.CharField(
                choices=[("male", "Male"), ("female", "Female")],
                default="male",
                max_length=10,
            ),
        ),
    ]
