from django.urls import reverse_lazy
from django.shortcuts import render,redirect,HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views import View
from django.views.generic import TemplateView,FormView,ListView,DetailView,UpdateView,DeleteView
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import AdminLoginForm,AddCategoryForm,UpdateCategoryForm,ProductForm,OrderUpdateForm
from .models import Category,Products
from Users.models import Order
from .decorator import admin_required
from django.utils.decorators import method_decorator


"""Here the Admin panal views are diaplayd """

# main page loding
@method_decorator(admin_required,name="dispatch")
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

@method_decorator(admin_required,name="dispatch")
class LogoutView(View):
  def get(self,request):
    logout(request)
    messages.warning(request,'Your LogOut !')
    return redirect('admin_login')


"""|| CATEGORY VIEWS ||"""

@method_decorator(admin_required,name="dispatch")
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
      return redirect('category_list')

@method_decorator(admin_required,name="dispatch")
class CategoryUpdateView(UpdateView):
  template_name='category_update.html'
  model=Category
  form_class=UpdateCategoryForm
  success_url=reverse_lazy('category_list')
  pk_url_kwarg='id'

  def form_valid(self, form):
    messages.success(self.request,'category updated.')
    return super().form_valid(form)
  
@method_decorator(admin_required,name="dispatch")
class CategoryDeleteView(View):
  def get(self,request,*args,**kwargs):
    try:
      cat=Category.objects.get(id=kwargs.get('id'))
      cat.delete()
      messages.success(self.request, f"Category '{cat.category_name}' deleted successfully.")
    except:
      messages.warning(request, "The category you are trying to delete does not exist.")
      return redirect('category_list')
    return redirect('category_list')


"""|| PRODUCTS VIEWS ||"""

@method_decorator(admin_required,name="dispatch")
class ProductView(ListView):
  model=Products
  template_name='products.html'
  context_object_name='products'
  
@method_decorator(admin_required,name="dispatch")
class AddProductView(FormView):
  template_name='add_product.html'
  form_class=ProductForm
  success_url=reverse_lazy('product_list')   # Redirect after successful product addition

  def form_valid(self, form):
    form.save() # Save the product to the database
    return super().form_valid(form)
  
@method_decorator(admin_required,name="dispatch")
class ProductUpdateView(UpdateView):
  model = Products
  form_class = ProductForm
  template_name = 'edit_product.html'
  success_url = reverse_lazy('product_list')

  def form_valid(self, form):
    messages.success(self.request,'Product updated.')
    return super().form_valid(form)

@method_decorator(admin_required,name="dispatch")
class ProductDeleteView(View):
  def get(self, request, *args, **kwargs):
    id = kwargs.get('pk')
    try:
      product = Products.objects.get(id=id)
      product.delete()
      messages.success(self.request, f"Product '{product.title}' deleted successfully.")
    except Products.DoesNotExist:
      messages.warning(request, "The product you are trying to delete does not exist.")
      return redirect('product_list')
    return redirect('product_list')


@method_decorator(admin_required,name="dispatch")
class NewOrderListView(ListView):
    model = Order
    template_name = "new_orders_list.html" 
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(status='order-placed').order_by('-date')
    
@method_decorator(admin_required,name="dispatch")
class OrderListView(ListView):
    model = Order
    template_name = "orders_list.html" 
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.all().order_by('-date')
    

@method_decorator(admin_required,name="dispatch")
class OrderDetailView(DetailView):
    model = Order
    template_name = "order_detail.html"
    context_object_name = "order"

    def post(self, request, *args, **kwargs):
        order = self.get_object()

        form = OrderUpdateForm(request.POST, instance=order)

        if form.is_valid():
            order = form.save(commit=False)  # Creates an Order instance without saving it
            order.expected_delivery_date = form.cleaned_data.get('expected_delivery_date') 
            order.status = form.cleaned_data.get('status')
            pro=Products.objects.get(id=order.product_id)
            pro.stock=(pro.stock)-(order.cart.quantity)
            order.save()
            

            self.send_order_status_email(order)

            return redirect(reverse_lazy('new_orders'))  # Redirect after saving

        return self.render_to_response(self.get_context_data(form=form))

    def send_order_status_email(self, order):
        subject = f"Your order status has been updated to {order.status}"
        message = f"Dear {order.user.first_name},\n\nYour order for {order.product.title} has been updated to '{order.status}'. Expected delivery date: {order.expected_delivery_date}.\n\nThank you!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [order.user.email]
        try:
            send_mail(subject, message, from_email, recipient_list)
            messages.success(self.request, 'Send email about order to user')
        except:
            messages.error(self.request, 'Connection Problem')
            return redirect(self.request.path_info) 
                  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "form" not in context:
            context["form"] = OrderUpdateForm(instance=self.get_object())
        return context