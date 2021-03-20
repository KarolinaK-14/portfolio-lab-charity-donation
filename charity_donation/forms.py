from django import forms
from django.contrib.auth.models import User

from charity_donation.models import Donation, Category, Institution


class RegisterForm(forms.ModelForm):

    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Powtórz hasło"}), label="")

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
            'password': forms.PasswordInput(attrs={'placeholder': 'Hasło'}),
        }
        labels = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': '',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        if password != repeat_password:
            msg = "Hasła muszą być takie same."
            self.add_error('password', msg)
            self.add_error('repeat_password', msg)


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

    # def clean(self):
    #     cleaned_data = super().clean()
    #     institution = cleaned_data.get('institution')
    #     institution_categories = cleaned_data.get('institution_categories')
    #     institution_categories = Category.object.filter(institution=institution)

