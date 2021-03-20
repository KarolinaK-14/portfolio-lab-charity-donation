from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, CreateView, TemplateView
from .forms import RegisterForm, DonationForm
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


class AddDonation(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        form = DonationForm()
        institutions = Institution.objects.all()
        return render(request, "form.html", {"form": form, 'institutions': institutions})

    def post(self, request):
        form = DonationForm(request.POST)
        if form.is_valid():
            categories = form.cleaned_data["categories"]
            quantity = form.cleaned_data["quantity"]
            institution = form.cleaned_data["institution"]
            address = form.cleaned_data["address"]
            city = form.cleaned_data["city"]
            zip_code = form.cleaned_data["zip_code"]
            phone_number = form.cleaned_data["phone_number"]
            pick_up_time = form.cleaned_data["pick_up_time"]
            pick_up_date = form.cleaned_data["pick_up_date"]
            pick_up_comment = form.cleaned_data["pick_up_comment"]
            donation = Donation(quantity=quantity,institution=institution,address=address,city=city,zip_code=zip_code,phone_number=phone_number,pick_up_date=pick_up_date,pick_up_time=pick_up_time,pick_up_comment=pick_up_comment)
            donation.save()
            donation.categories.set(categories)
            donation.save()
            return redirect('donation_confirmation')
        return render(request, "form.html", {"form": form, 'institutions': institutions})


class DonationConfirmation(TemplateView):
    template_name = "form-confirmation.html"


class Login(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = reverse_lazy("landing_page")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        login(self.request, user=user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('/register/#register-form')


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
