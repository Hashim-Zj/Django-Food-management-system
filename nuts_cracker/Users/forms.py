from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Cart, Order, Profile


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter Password"}
        ),
        help_text=None,
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        ),
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
            "username": forms.TextInput(attrs={"class": "form-control mb-4"}),
            "password": forms.PasswordInput(attrs={"class": "form-control mb-1"}),
        }
        help_texts = {"username": None}


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-4", "placeholder": "User Name"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control mb-1", "placeholder": "Email Id"}
        ),
    )


class PasswordResetForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=("New Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-4", "placeholder": "Enter New Password"}
        ),
        help_text=None,
    )
    new_password2 = forms.CharField(
        label=("Confirm Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-1", "placeholder": "Confirm your Password"}
        ),
        help_text=None,
    )

    class Meta:
        model = User
        fields = ("new_password1", "new_password2")


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control mb-1",
                "placeholder": "Enter your email",
                "required": "required",
            }
        ),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-1",
                "placeholder": "Enter your first name",
                "required": "required",
            }
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=254,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-1",
                "placeholder": "Enter your last name",
            }
        ),
    )

    class Meta:
        model = Profile
        fields = [
            "mobile_number",
            "address",
            "pin_code",
        ]
        widgets = {
            "mobile_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Mobile Number",
                    "required": "required",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Address",
                    "required": "required",
                }
            ),
            "pin_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "PIN Code",
                    "required": "required",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ProfileForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["email"].initial = user.email

            self.fields["email"].disabled = True


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ["quantity"]
        widgets = {"quantity": forms.NumberInput(attrs={"class": "form-control"})}
