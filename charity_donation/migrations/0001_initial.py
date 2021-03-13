# Generated by Django 3.1.7 on 2021-03-13 12:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('fundacja', 'fundacja'), ('organizacja pozarządowa', 'organizacja pozarządowa'), ('zbiórka lokalna', 'zbiórka lokalna')], default='fundacja', max_length=60)),
                ('categories', models.ManyToManyField(to='charity_donation.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('address', models.CharField(max_length=60)),
                ('phone_number', models.CharField(max_length=12, verbose_name=[django.core.validators.RegexValidator(message='Podaj poprawny numer telefonu w formacie +99999999999', regex='^\\+?\\d{9,12}$')])),
                ('city', models.CharField(max_length=60)),
                ('zip_code', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(message='Podaj poprawny kod pocztowy w formacie 99-999', regex='^\\d{2}-\\d{3}$')])),
                ('pick_up_date', models.DateField()),
                ('pick_up_time', models.TimeField()),
                ('pick_up_comment', models.TextField()),
                ('categories', models.ManyToManyField(to='charity_donation.Category')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charity_donation.institution')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
