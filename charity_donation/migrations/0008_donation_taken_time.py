# Generated by Django 3.1.7 on 2021-03-28 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("charity_donation", "0007_remove_donation_taken_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="donation",
            name="taken_time",
            field=models.DateTimeField(default="2021-01-01 20:00"),
            preserve_default=False,
        ),
    ]
