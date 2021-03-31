from django.contrib.auth.password_validation import password_validators_help_texts, password_validators_help_text_html, \
    validate_password

from charity_donation.models import Donation, Category, Institution

from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Hasło"}), validators=[validate_password], label="")
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Powtórz hasło"}), validators=[validate_password], label="")
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'repeat_password'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),

        }
        labels = {
            'first_name': '',
            'last_name': '',
            'email': '',

        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")
        email = cleaned_data.get('email')

        if password != repeat_password:
            msg = "Hasła muszą być takie same."
            self.add_error('password', msg)
            self.add_error('repeat_password', msg)

        if User.objects.get(email=email):
            self.add_error('email', "Podany email jest już zajęty.")


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['categories', 'quantity', 'institution', 'address', 'city', 'zip_code', 'phone_number', 'pick_up_date', 'pick_up_time', 'pick_up_comment']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
            'quantity': forms.NumberInput(attrs={'step': 1, 'min': 1}),
            'institution': forms.RadioSelect(),
            'phone_number': forms.TextInput(attrs={'type': 'phone'}),
            'pick_up_date': forms.DateInput(attrs={'type': 'date'}),
            'pick_up_time': forms.TimeInput(attrs={'type': 'time'}),
            'pick_up_comment': forms.Textarea(attrs={'rows': 5}),
        }
        help_texts = {
            'categories': 'Wybierz co najmniej jedną kategorię. Wymagane.',
            'quantity': 'Podaj liczbę. Wymagane.',
            'institution': 'Wybierz jedną organizację. Wymagane.',
            'address': 'Wymagane.',
            'zip_code': 'Wymagane.',
            'city': 'Wymagane.',
            'phone_number': 'Wymagane.',
            'pick_up_date': 'Wymagane.',
            'pick_up_time': 'Wymagane.',
        }


class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Imię"})
    )
    surname = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Nazwisko"})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Wiadomość", "rows": "1"})
    )