from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator


class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


INSTITUTIONS = (
    ('fundacja', 'fundacja'),
    ('organizacja pozarządowa', 'organizacja pozarządowa'),
    ('zbiórka lokalna', 'zbiórka lokalna'),
)


class Institution(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    type = models.CharField(max_length=60, choices=INSTITUTIONS, default='fundacja')
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=12, validators=[RegexValidator(regex=r'^\+?\d{9,12}$', message='Podaj poprawny numer telefonu w formacie +99999999999')])
    city = models.CharField(max_length=60)
    zip_code = models.CharField(max_length=6, validators=[RegexValidator(regex=r'^\d{2}-\d{3}$', message='Podaj poprawny kod pocztowy w formacie 99-999')])
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return f"dla {self.institution.name}"
