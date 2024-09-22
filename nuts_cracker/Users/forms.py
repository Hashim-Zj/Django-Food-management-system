from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cart, Order, Profile


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text=None,
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text=None,
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
        help_texts = {"username": None}


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }
        help_texts = {"username": None}


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)  # 254 is the maximum length of an email address


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "address",
            "pin_code",
            "mobile_number",
            "email",
            "first_name",
            "last_name",
        ]
        widgets = {
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "pin_code": forms.TextInput(attrs={"class": "form-control"}),
            "mobile_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ["quantity"]
        widgets = {"quantity": forms.NumberInput(attrs={"class": "form-control"})}


class OrderPlaceForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["address", "phone"]
        widgets = {
            "address": forms.Textarea(attrs={"class": "form-control"}),
            "phone": forms.NumberInput(attrs={"class": "form-control"}),
        }
