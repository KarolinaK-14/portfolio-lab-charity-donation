# Generated by Django 3.1.7 on 2021-03-28 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("charity_donation", "0004_auto_20210326_1831"),
    ]

    operations = [
        migrations.AlterField(
            model_name="donation",
            name="pick_up_comment",
            field=models.TextField(blank=True, null=True),
        ),
    ]
