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

    help_texts={
      'username':None
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
      "status":forms.CheckboxInput(attrs={"class":"form-check-input"}),
    }


class ProductForm(forms.ModelForm):
  class Meta:
    model=Products
    fields=['title','description','quantity','category','price','image']
    widgets = {
      'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product title'}),
      'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter product description'}),
      'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity eg: 500g'}),
      'stoke':forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter totel stoke'}),
      'category': forms.Select(attrs={'class': 'form-control'}),
      'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
      'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
    }
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    # category choices from Category model
    self.fields['category'].queryset=Category.objects.filter(status=True)