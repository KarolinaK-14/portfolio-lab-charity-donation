from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class LandingPage(TemplateView):
    template_name = "index.html"


class AddDonation(TemplateView):
    template_name = "form.html"


class Login(TemplateView):
    template_name = "login.html"


class Register(TemplateView):
    template_name = "register.html"
