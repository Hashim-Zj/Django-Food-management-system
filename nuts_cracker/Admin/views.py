from django.shortcuts import render,redirect,HttpResponse
from django.views.generic import TemplateView,FormView
from django.contrib.auth import login,logout,authenticate
from .forms import AdminLoginForm
from .models import Category

# Create your views here.

class AdminHomeView(TemplateView):
  template_name='base.html'

class AdminLoginView(FormView):
  form_class=AdminLoginForm
  template_name='admin_login.html'

  def post(self,request):
    uname=request.POST.get("username")
    psw=request.POST.get("password")
    user=authenticate(request,username=uname,password=psw)
    print(user.is_staff)
    if user.is_staff:
      login(request,user)
      return redirect('admin_index')
    else:
      return HttpResponse("NO")
