from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import login,logout,aauthenticate
from django.contrib.auth.views import LoginView
from django.views.generic import ListView,DetailView,CreateView
from django.views import View
from .forms import UserRegisterForm
from Admin.models import Products
from .models import OTP


#  || Main Page 

class MainDisplayView(ListView):
  model = Products
  template_name = 'main.html'
  context_object_name = 'products'


#  || Authentiction Views 

class UserRegisterView(CreateView):
  template_name='authentic/registration.html'
  form_class=UserRegisterForm
  success_url=reverse_lazy('otp_verification')

  def form_valid(self, form):
    response= super().form_valid(form)
    user=form.save()
    otp=OTP.objects.create(user=user)
    # send OTP to coresponding email
    send_mail(
      'Your OTP Code for Registaring in Nutcraker'
      'xxxxxx'
      'form admin@nutracker\'s'
      f'OTP code is :[ {otp.code} ].'
      "Don't share This !",
      [user.email],
      fail_sailently=False
    )
    return response
  
class OTPVerificationView(View):
  def get(self,request):
    return render(request,'authentic/otp_verification.html')

  def post(self,request):
    otp_code=request.POST.get('otp_code')
    try:
      otp= OTP.objects.get(code=otp_code, used=False)
      user=otp.user
      user.is_active=True
      user.save()
      login(request,user)
      return redirect('index')
    except OTP.DoesNotExist:
      return render(request, 'authentic/otp_verification.html',{'error':'Invalid OTP'})

class UserLoginView(LoginView):
  template_name = 'registration/login.html'


#  || Product

class ProductDetailView(DetailView):

  model = Products
  template_name = 'product_detail.html'
  context_object_name = 'product'


def add_to_cart(request, pk):
  # Add your cart logic here
  messages.success(request, "Product added to cart.")
  return redirect('index')

def place_order(request, pk):
  # Add your order logic here
  messages.success(request, "Order placed successfully.")
  return redirect('index')