
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Ticket
from django.contrib.auth.forms import PasswordChangeForm

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(
        required=True,
        label='Full Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Full Name'})
    )
    email = forms.CharField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email'})
    )
    password1 = forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Password'}),
        help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField(
        required=True,
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Your Password'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex. Fariha_6007'})
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match.')

        validate_password(password1, self.instance)
        return cleaned_data

class LoginForm(AuthenticationForm):
   username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
   password = forms.CharField(label=("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['request_type', 'priority', 'title', 'description', 'attachment']
        widgets = {
            'request_type': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label="Enter your Gmail address",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com'}),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("Only Gmail addresses are accepted for password recovery.")
        return email
class SolutionForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['solution_text']
        widgets = {
            'solution_text': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your solution here...'})
        }
