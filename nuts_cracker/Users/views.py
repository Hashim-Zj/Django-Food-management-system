from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
import random
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login, logout, authenticate
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView
from .forms import (
    UserRegisterForm,
    UserLoginForm,
    AddToCartForm,
    ProfileForm,
    PasswordResetRequestForm,
)
from django.contrib.auth.models import User
from Admin.models import Products
from .models import OTP, Cart, Order, Wishlist
from .decorator import login_required
from django.utils.decorators import method_decorator


# || CUSTOM VIEWS
def non_existing_view(request):
    return HttpResponseNotFound("This page does not exist.")


# SEND OTP
def send_otp(user, subject, message_template, recipient):
    # Get or create the OTP
    otp, created = OTP.objects.get_or_create(user=user)

    if otp.used:
        otp.code = str(random.randint(100000, 999999))
        otp.created_at = timezone.now()
        otp.used = False
        otp.save()
    else:
        otp.created_at = timezone.now()
        otp.save()

    # Format the message with the OTP code
    message = message_template.format(otp_code=otp.code)

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient,
        fail_silently=False,
    )


# || OTP VERIFICATIONS
class OTPVerificationView(View):
    def get(self, request):
        return render(request, "authentic/otp_verification.html")

    def post(self, request):
        otp_code = request.POST.get("otp_code")
        try:
            otp = OTP.objects.get(code=otp_code, used=False)
            # Check if the OTP is valid
            if otp.is_valid():
                otp.used = True
                otp.save()

                user = otp.user
                user.is_active = True
                user.save()

                login(request, user)
                messages.success(request,"OTP verification Successfull.")
                return redirect("redirect_url","index")
            else:
                messages.error(request,"Invalid OTP.\n send new request")

        except OTP.DoesNotExist:
            messages.warning(request, "OTP Expaird")
            return render(
                request, "authentic/otp_verification.html", {"error": "Invalid OTP"}
            )
        
def resend_otp(request):
    if request.method == "POST":  # Ensure it's a POST request
        user = request.user  # Get the currently logged-in user
        send_otp(user, "Your New OTP Code", "Your OTP code is {otp_code}.",[user.email])
        messages.success(request, "A new OTP has been sent to your email.")
    else:
        messages.error(request, "Invalid request method.")

    return render(request, "authentic/otp_verification.html")

#  || Main Page
class MainDisplayView(ListView):
    model = Products
    template_name = "main.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if user is authenticated before querying Wishlist
        if self.request.user.is_authenticated:
            wishlist_products = Wishlist.objects.filter(
                user=self.request.user
            ).values_list("product", flat=True)
        else:
            wishlist_products = []

        context["wishlist_products"] = wishlist_products
        return context


#  || Authentiction Views
class UserRegisterView(CreateView):
    template_name = "authentic/registration.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy(f'/otp-verification?redirect_url=index')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        if user:
            send_otp(
                user,
                "Your OTP Code for Registering to Nutcracker",
                "Hi,\nYour OTP code is: [{otp_code}].\n Valid for the next 5 minutes.\n Do not share this code with anyone",
                [form.cleaned_data["email"]],
            )
            messages.success(self.request, "OTP has been sent to your email.")
            return response
        else:
            return redirect('register')

class UserLoginView(FormView):
    template_name = "authentic/user_login.html"
    form_class = UserLoginForm

    def post(self, request, *args, **kwargs):
        uname = request.POST.get("username")
        psw = request.POST.get("password")
        user = authenticate(request, username=uname, password=psw)
        if user:
            login(request, user)
            send_otp(
                user,
                "Your OTP Code for Login",
                "Hi,\nYour OTP code is: [{otp_code}].\n Valid for the next 5 minutes.\n Do not share this code with anyone",
                [user.email],
            )
            messages.success(request,"OTP for verification is send to you email")
            return redirect(f'/otp-verification?redirect_url=index') # Redirect to OTP verification page amd index
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")  # Redirect to login page

    # def post(self, request):
    #     uname = request.POST.get("username")
    #     psw = request.POST.get("password")
    #     user = authenticate(request, username=uname, password=psw)
    #     if user:
    #         login(request, user)
    #         messages.success(request, "Login Successful")
    #         return redirect("index")
    #     else:
    #         messages.success(request, "Invalid credaintials")
    #         return redirect("index")

@method_decorator(login_required, name="dispatch")
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logout Successful")
        return redirect("index")


class PasswordResetRequestView(FormView):
    template_name = "authentic/password_reset_request.html"
    form_class = PasswordResetRequestForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            send_otp(
                user,
                "Your OTP Code for Password Reset",
                "Hi,\nYour OTP code is: [{otp_code}]. Valid for the next 10 minutes.",
                [user.email],
            )
            messages.success(self.request, "OTP has been sent to your email.")
            return redirect(f'/otp-verification?redirect_url=reset_password')
        else:
            messages.error(self.request, "User with this email does not exist.")
            return redirect('login')

@method_decorator(login_required, name="dispatch")
class ProfileCreateView(FormView):
    template_name = "profile_view.html"
    form_class = ProfileForm
    success_url = reverse_lazy("index")  # Replace with your desired redirect

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial["email"] = user.email
        initial["first_name"] = user.first_name
        initial["last_name"] = user.last_name
        return initial

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user  # Associate profile with logged-in user
        profile.save()
        return super().form_valid(form)


#  || Product
@method_decorator(login_required, name="dispatch")
class ProductDetailView(DetailView):
    model = Products
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AddToCartForm()  # Add the form to the context
        return context


@method_decorator(login_required, name="dispatch")
class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        product = get_object_or_404(Products, pk=kwargs.get("pk"))
        qty = int(request.POST.get("quantity", 1))  # Default to 1 if not provided

        # Check if the product is already in the cart
        cart_item, created = Cart.objects.get_or_create(
            user=user, product=product, status="in-cart", defaults={"quantity": qty}
        )

        if not created:
            # If the cart item already exists, update the quantity
            cart_item.quantity += qty
            cart_item.save()
            messages.success(
                request, f"Updated quantity for {product.title} in your cart."
            )
        else:
            messages.success(request, f"Added {product.title} to your cart.")

        return redirect("index")


@method_decorator(login_required, name="dispatch")
class CartListView(ListView):
    model = Cart
    template_name = "cart_list.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user, status="in-cart").order_by(
            "-date"
        )


# || WishList Views
@method_decorator(login_required, name="dispatch")
class WishlistView(ListView):
    model = Wishlist
    template_name = "wishlist.html"
    context_object_name = "wishlist_items"

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


@method_decorator(login_required, name="dispatch")
class AddToWishlistView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        product = Products.objects.get(id=kwargs.get("pk"))
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=user, product=product
        )

        if created:
            messages.info(request, "Product added to wishlist.")
        else:
            messages.info(request, "Product is already in your wishlist.")
        return redirect("index")  # Adjust this to your desired redirect


@method_decorator(login_required, name="dispatch")
class RemoveFromWishlistView(View):
    def post(self, request, *args, **kwargs):
        product = Products.objects.get(id=kwargs.get("pk"))
        wishlist_item = Wishlist.objects.filter(
            user=request.user, product=product
        ).first()

        if wishlist_item:
            wishlist_item.delete()
            messages.info(request, "Product removed from your Wishlist.")

        # Redirect back to the page the user was on using HTTP_REFERER
        return redirect(request.META.get("HTTP_REFERER", "index"))


# class OrderPlaceView(FormView):
#     template_name = "order_place.html"
#     form_class = OrderPlaceForm

#     def post(self, request, *args, **kwargs):
#         in_cart = get_object_or_404(Cart, id=kwargs.get("id"))
#         user = request.user
#         email = user.email
#         address = request.POST.get("address")
#         phone = request.POST.get("phone")

#         Order.objects.create(
#             user=user, product_name=in_cart.product, address=address, phone=phone
#         )
#         in_cart.status = "order-placed"
#         in_cart.save()

#         # Assuming you have a send_mail function set up
#         send_mail(
#             "E-Bay.com",
#             "Your order was placed successfully!",
#             settings.EMAIL_HOST_USER,
#             [email],
#         )
#         messages.success(request, "Order placed successfully")
#         return redirect("cartlist_view")


# class UserOrderListView(View):
#     def get(self, request):
#         all_orders = Order.objects.filter(user=request.user).order_by("-date")
#         delivered = Order.objects.filter(user=request.user, status="delivered")
#         return render(
#             request,
#             "user_order_list.html",
#             {"all_orders": all_orders, "delivered": delivered},
#         )

