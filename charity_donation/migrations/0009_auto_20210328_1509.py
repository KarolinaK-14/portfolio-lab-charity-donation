# Generated by Django 3.1.7 on 2021-03-28 13:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("charity_donation", "0008_donation_taken_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="donation",
            name="phone_number",
            field=models.CharField(
                max_length=12,
                validators=[
                    django.core.validators.RegexValidator(regex="^\\+?\\d{9,12}$")
                ],
            ),
        ),
        migrations.AlterField(
            model_name="donation",
            name="taken_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="donation",
            name="zip_code",
            field=models.CharField(
                max_length=6,
                validators=[
                    django.core.validators.RegexValidator(regex="^\\d{2}-\\d{3}$")
                ],
            ),
        ),
    ]
