from django.contrib import admin, messages
from .models import Category, Institution, Donation
from django.contrib.admin import helpers

admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)

