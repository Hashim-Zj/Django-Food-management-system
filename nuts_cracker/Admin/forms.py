from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category,Products

# Forms Needed in Admin panals
class AdminLoginForm(forms.ModelForm):
  class Meta:
    model=User
    fields=["username","password"]
    widgets={
      "username":forms.TextInput(attrs={"class":"form-control"}),
      "password":forms.PasswordInput(attrs={"class":"form-control"})
    }

# || CATEGORY SECTION FORMS
class AddCategoryForm(forms.ModelForm):
  class Meta:
    model=Category
    fields=["category_name"]
    widgets={
      "category_name":forms.TextInput(attrs={"class":"form-control my-3","placeholder":"Enter category name"})
    }

class UpdateCategoryForm(forms.ModelForm):
  class Meta:
    model=Category
    fields=["category_name","status"]
    widgets={
      "category_name":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter category name"}),
      "status":forms.CheckboxInput(attrs={"class":"form-control","placeholder":"Enter category name"}),
    }