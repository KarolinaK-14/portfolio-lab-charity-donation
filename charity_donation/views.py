from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User as U
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect, resolve_url
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView, CreateView, TemplateView, DetailView, UpdateView
from .forms import RegisterForm, DonationForm, ContactForm
from .models import Institution, Donation
from django.db.models import Sum
from django.core.paginator import Paginator
from django.core.mail import EmailMessage, send_mail, mail_admins

from .tokens import account_activation_token


class LandingPage(View):
    def get(self, request):
        paginator1 = Paginator(Institution.objects.filter(type='fundacja'), 5)
        page1 = request.GET.get('page1')
        paginator2 = Paginator(Institution.objects.filter(type='organizacja pozarządowa'), 5)
        page2 = request.GET.get('page2')
        paginator3 = Paginator(Institution.objects.filter(type='zbiórka lokalna'), 5)
        page3 = request.GET.get('page3')
        form = ContactForm()

        context = {'donations': Donation.objects.all().aggregate(Sum("quantity"))["quantity__sum"],
                   'institutions': Institution.objects.filter(donation__isnull=False).count(),
                   'foundations': paginator1.get_page(page1),
                   'non_gov_organizations': paginator2.get_page(page2),
                   'collections': paginator3.get_page(page3),
                   "form": form
                   }
        return render(request, "index.html", context=context)

    def post(self, request):

        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            surname = form.cleaned_data["surname"]
            admins = U.objects.filter(is_staff=True, is_superuser=True)
            send_mail(
                subject=f"Oddam w dobre ręce - Wiaodmość od użytkownika {name.capitalize()} {surname.capitalize()}",
                message=form.cleaned_data["message"],  # message body
                from_email=request.user.email,  # from
                recipient_list=[a.email for a in admins],  # to
            )
            form = ContactForm()  # once message sent, clear the form
            return render(request, "index.html", {"form": form, 'name': name})
        return render(request, "index.html", {"form": form})

class AddDonation(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    def get(self, request):
        form = DonationForm()
        institutions = Institution.objects.all()
        return render(request, "form.html", {"form": form, 'institutions': institutions})

    def post(self, request):
        form = DonationForm(request.POST)
        institutions = Institution.objects.all()
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
            donation = Donation(quantity=quantity,institution=institution,address=address,city=city,zip_code=zip_code,phone_number=phone_number,pick_up_date=pick_up_date,pick_up_time=pick_up_time,pick_up_comment=pick_up_comment,user=request.user)
            donation.save()
            donation.categories.set(categories)
            donation.save()
            return redirect('donation_confirmation')
        return render(request, "form.html", {"form": form, 'institutions': institutions})


class DonationConfirmation(TemplateView):
    template_name = "form-confirmation.html"


class Login(FormView):
    form_class = AuthenticationForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("landing_page")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        login(self.request, user=user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('/register/#register-form')


class Register(View):
    form_class = RegisterForm
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(form.cleaned_data["password"])
            user.username = form.cleaned_data["email"]
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Oddam w dobre ręce - aktywuj konto'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)


            return render(request, 'email-confirmation.html')

        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = U.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, U.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            return redirect('landing_page')
        else:
            return render(request, 'email-confirmation-failed.html')


class User(View):
    def get(self, request):
        user_donations = request.user.donation_set.order_by('is_taken', '-pick_up_time')
        return render(request, 'user_profile.html', {"user_donations": user_donations})


class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("user")
    template_name = "password_change.html"


class UserUpdate(View):

    def get(self, request):
        form = RegisterForm(initial={'first_name': request.user.first_name, 'last_name': request.user.last_name, 'email': request.user.email} )
        return render(request, "user_profile_update.html", {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            success = request.user.check_password(form.cleaned_data['password'])
            if success:
                request.user.first_name = first_name
                request.user.last_name = last_name
                request.user.email = email
                request.user.save()
                return redirect('user')
        else:
            return redirect('edit-user')


class Archive(View):
    def post(self, request, pk):
        donation = request.user.donation_set.get(pk=pk)
        if "archive-add" in request.POST:
            donation.is_taken = True
            donation.taken_time = timezone.now()
            donation.save()
            return redirect('user')
        if "archive-remove" in request.POST:
            donation.is_taken = False
            donation.save()
            return redirect('user')







