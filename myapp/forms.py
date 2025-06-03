
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.password_validation import validate_password


class SignUpForm(UserCreationForm):
     password1=forms.CharField(required=True,label='Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}), help_text=password_validation.password_validators_help_text_html())
     password2=forms.CharField(required=True,label='Confirm password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}))
     email=forms.CharField(required=True,label='Email',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Your Email'}))
     class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
        widgets={'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your name'})}
     def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match.')

        validate_password(password1, self.instance)  # Validate password complexity

        return cleaned_data



class LoginForm(AuthenticationForm):
   username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
   password = forms.CharField(label=("password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))