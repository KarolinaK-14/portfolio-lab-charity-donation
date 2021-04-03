import datetime

from django.contrib.auth.models import User as U
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


INSTITUTIONS = (
    ("fundacja", "fundacja"),
    ("organizacja pozarządowa", "organizacja pozarządowa"),
    ("zbiórka lokalna", "zbiórka lokalna"),
)


class Institution(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    type = models.CharField(max_length=60, choices=INSTITUTIONS, default="fundacja")
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


def validate_date(visit_date):
    """Raise the error if the given date has already passed."""
    if visit_date < datetime.date.today():
        raise ValidationError("Ale to już było! Wybierz datę z przyszłości.")


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=60)
    phone_number = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(
                regex=r"^\+?\d{9,12}$",
                message="Przykładowy poprawny format numeru telefonu: 111222333",
            )
        ],
    )
    city = models.CharField(max_length=60)
    zip_code = models.CharField(
        max_length=6,
        validators=[
            RegexValidator(
                regex=r"^\d{2}-\d{3}$",
                message="Przykładowy poprawny format kodu pocztowego: 00-000",
            )
        ],
    )
    pick_up_date = models.DateField(validators=[validate_date])
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        U, on_delete=models.CASCADE, null=True, blank=True, default=None
    )
    is_taken = models.BooleanField(default=False)
    taken_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"dla {self.institution.name} od {self.user}"


class Profile(models.Model):
    user = models.OneToOneField(U, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=U)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
