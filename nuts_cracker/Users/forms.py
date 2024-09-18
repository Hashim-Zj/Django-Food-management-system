from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

class UserRegisterForm(UserCreationForm):
  password1 = forms.CharField(
    label="Password",
    strip=False,
    widget=forms.PasswordInput(attrs={"class": "form-control"}),
    help_text=password_validation.password_validators_help_text_html(),
  )
  password2 = forms.CharField(
    label="Password confirmation",
    strip=False,
    widget=forms.PasswordInput(attrs={"class": "form-control"}),
    help_text="Enter the same password as before, for verification.",
  )

  class Meta:
    model = User
    fields = ["username", "email", "password1", "password2"]
    widgets = {
      'username': forms.TextInput(attrs={"class": "form-control"}),
      'email': forms.EmailInput(attrs={"class": "form-control"}),
    }
    