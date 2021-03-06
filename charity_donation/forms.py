from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.password_validation import validate_password

from django.core.exceptions import ValidationError

from charity_donation.models import Donation

from django import forms
from django.contrib.auth.models import User


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Imię"}))
    surname = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nazwisko"}))
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Wiadomość", "rows": "1"})
    )


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Hasło"}),
        validators=[validate_password],
        label="",
    )
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Powtórz hasło"}),
        validators=[validate_password],
        label="",
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "repeat_password"]

        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Imię"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Nazwisko"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }
        labels = {
            "first_name": "",
            "last_name": "",
            "email": "",
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")
        email = cleaned_data.get("email")

        if password != repeat_password:
            msg = "Hasła w obu polach nie są zgodne."
            self.add_error("password", msg)
            self.add_error("repeat_password", msg)

        try:
            if User.objects.get(email=email):
                self.add_error("email", "Podany email jest już zajęty.")
        except User.DoesNotExist:
            pass


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("Użytkownik z takim adresem e-mail nie istnieje.")
        return email


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = [
            "categories",
            "quantity",
            "institution",
            "address",
            "city",
            "zip_code",
            "phone_number",
            "pick_up_date",
            "pick_up_time",
            "pick_up_comment",
        ]
        widgets = {
            "categories": forms.CheckboxSelectMultiple(),
            "quantity": forms.NumberInput(attrs={"step": 1, "min": 1}),
            "institution": forms.RadioSelect(),
            "phone_number": forms.TextInput(attrs={"type": "phone"}),
            "pick_up_date": forms.DateInput(attrs={"type": "date"}),
            "pick_up_time": forms.TimeInput(attrs={"type": "time"}),
            "pick_up_comment": forms.Textarea(attrs={"rows": 5}),
        }
        help_texts = {
            "categories": "Wybierz co najmniej jedną kategorię. Pole wymagane.",
            "quantity": "Podaj liczbę. Pole wymagane.",
            "institution": "Wybierz jedną organizację. Pole wymagane.",
            "address": "Pole wymagane.",
            "zip_code": "Pole wymagane.",
            "city": "Pole wymagane.",
            "phone_number": "Pole wymagane.",
            "pick_up_date": "Pole wymagane.",
            "pick_up_time": "Pole wymagane.",
        }
