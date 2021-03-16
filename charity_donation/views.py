from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView
from .forms import RegisterForm
from .models import Institution, Donation
from django.db.models import Sum
from django.core.paginator import Paginator


class LandingPage(View):
    def get(self, request):
        paginator1 = Paginator(Institution.objects.filter(type='fundacja'), 5)
        page1 = request.GET.get('page1')
        paginator2 = Paginator(Institution.objects.filter(type='organizacja pozarządowa'), 5)
        page2 = request.GET.get('page2')
        paginator3 = Paginator(Institution.objects.filter(type='zbiórka lokalna'), 5)
        page3 = request.GET.get('page3')
        context = {'donations': Donation.objects.all().aggregate(Sum("quantity"))["quantity__sum"],
                   'institutions': Institution.objects.filter(donation__isnull=False).count(),
                   'foundations': paginator1.get_page(page1),
                   'non_gov_organizations': paginator2.get_page(page2),
                   'collections': paginator3.get_page(page3),
                   }
        return render(request, "index.html", context=context)


class AddDonation(TemplateView):
    template_name = "form.html"


class Register(FormView):
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data["password"])
        user.username = form.cleaned_data["email"]
        user.save()
        return super().form_valid(form)
