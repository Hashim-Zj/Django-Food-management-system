from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category,Products
from Users.models import Order

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
    fields=['title','description','quantity','stock','category','mrp','price','image']
    widgets = {
      'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product title', 'required': True}),
      'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter product description'}),
      'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity eg: 500g', 'required': True}),
      'stock':forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter totel stock', 'required': True}),
      'category': forms.Select(attrs={'class': 'form-control', 'required': True}),
      'mrp': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter MRP', 'required': True}),
      'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price', 'required': True}),
      'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'required': True}),

    }
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    # category choices from Category model
    self.fields['category'].queryset=Category.objects.filter(status=True)

  def clean(self):
      cleaned_data = super().clean()
      title = cleaned_data.get('title')
      price = cleaned_data.get('price')
      stock = cleaned_data.get('stock')
      mrp=cleaned_data.get('mrp')

      # Custom validation example
      if not title:
        self.add_error('title', 'Title cannot be empty.')

      if mrp is not None and price is not None and price > mrp:
        self.add_error('price', 'Price must be less than or equal to MRP.')

      if stock is None or stock < 0:
        self.add_error('stock', 'Stock cannot be negative.')

      return cleaned_data
  

class OrderUpdateForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('dispatched', 'Dispatched'),
        ('cancelled', 'Cancelled'),
        ('delivered', 'Delivered'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ['status', 'expected_delivery_date']
        widgets = {
            'expected_delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }