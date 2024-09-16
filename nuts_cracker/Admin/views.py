from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from django.views.generic import TemplateView,FormView,ListView,DetailView,UpdateView,DeleteView
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import AdminLoginForm,AddCategoryForm,UpdateCategoryForm
from .models import Category,Products


"""Here the Admin panal views are diaplayd """

# main page loding
class AdminHomeView(TemplateView):
  template_name='base.html'

# Admin authentication 
class AdminLoginView(FormView):
  form_class=AdminLoginForm
  template_name='admin_login.html'

  def post(self,request):
    uname=request.POST.get("username")
    psw=request.POST.get("password")
    try:
      user=authenticate(request,username=uname,password=psw)
      if (user.is_superuser):
        login(request,user)
        messages.success(request, 'Login successfull.')
        return redirect('admin_index')
    except:
      messages.warning(request, 'Please fill the corect datas.')
      return redirect('admin_login')
    
class LogoutView(View):
  def get(self,request):
    logout(request)
    messages.warning(request,'Your LogOut !')
    return redirect('admin_index')


"""|| CATEGORY VIEWS ||"""

class CategoryView(ListView):
  model=Category
  template_name='category.html'
  form_class=AddCategoryForm
  context_object_name='category'

#  Override the get_queryset to filter categories with status=True
  def get_queryset(self):
    return Category.objects.filter(status=True)
  
# Override get_context_data to pass the form to the template
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['form'] = self.form_class()
      return context

# Handle form submission
  def post(self, request, *args, **kwargs):
      form = self.form_class(request.POST)
      if form.is_valid():
          category_name = form.cleaned_data['category_name']
          Category.objects.create(category_name=category_name, status=True)
      return redirect('category_view')

class CategoryUpdateView(UpdateView):
  template_name='category_update.html'
  model=Category
  form_class=UpdateCategoryForm
  success_url=reverse_lazy('category_view')
  pk_url_kwarg='id'

  def form_valid(self, form):
    messages.success(self.request,'category updated.')
    return super().form_valid(form)
  
class CategoryDeleteView(View):
  def get(self,request,*args,**kwargs):
    try:
      cat=Category.objects.get(id=kwargs.get('id'))
      cat.delete()
      messages.success(self.request, f"Category '{cat.category_name}' deleted successfully.")
    except:
      messages.warning(request, "The category you are trying to delete does not exist.")
      return redirect('category_view')
    return redirect('category_view')


# class CategoryDeleteView(DeleteView):
  # model = Category
  # success_url = reverse_lazy('category_view')
  # pk_url_kwarg='id'

  # def delete(self, request, *args, **kwargs):
  #   self.object=self.get_object()
  #   try:
  #     print(self.object)
  #     self.object.delete()

  #   except Exception as e:
  #     messages.error(self.request, f'Failed to delete category : {e}')
  #     return super().delete(request,*args,**kwargs)
    
  #   messages.success(self.request, f"Category '{self.object.category_name}' deleted successfully.")
  #   return super().delete(request, *args, **kwargs)


"""|| PRODUCTS VIEWS ||"""

class ProductView(ListView):
  model=Products
  pass

class 