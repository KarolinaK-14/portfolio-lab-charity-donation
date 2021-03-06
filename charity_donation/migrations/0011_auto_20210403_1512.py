# Generated by Django 3.1.7 on 2021-04-03 13:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("charity_donation", "0010_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="donation",
            name="phone_number",
            field=models.CharField(
                max_length=12,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Przykładowy poprawny format numeru telefonu: 111222333",
                        regex="^\\+?\\d{9,12}$",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="donation",
            name="zip_code",
            field=models.CharField(
                max_length=6,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Przykładowy poprawny format kodu pocztowego: 00-000",
                        regex="^\\d{2}-\\d{3}$",
                    )
                ],
            ),
        ),
    ]
