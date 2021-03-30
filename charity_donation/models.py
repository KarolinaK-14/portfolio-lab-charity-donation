from django.contrib.auth.models import User as U
from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    phone_number = models.CharField(max_length=12, validators=[RegexValidator(regex=r'^\+?\d{9,12}$')])
    city = models.CharField(max_length=60)
    zip_code = models.CharField(max_length=6, validators=[RegexValidator(regex=r'^\d{2}-\d{3}$')])
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey(U, on_delete=models.CASCADE, null=True, blank=True, default=None)
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
