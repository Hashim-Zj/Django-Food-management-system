from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.contrib.auth import login, logout, authenticate
from .decorator import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseNotFound
import random
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView
from .forms import (
    UserRegisterForm,
    UserLoginForm,
    AddToCartForm,
    ProfileForm,
    ForgotPasswordForm,
    PasswordResetForm,
)
from django.contrib.auth.models import User
from Admin.models import Products
from .models import OTP, Cart, Order, Wishlist,Profile


# || CUSTOM VIEWS
def non_existing_view(request):
    return HttpResponseNotFound("This page does not exist.")


# SEND OTP
def send_otp(user, subject, message_template, recipient):
    # Get or create the OTP
    otp, created = OTP.objects.get_or_create(user=user)

    otp.code = str(random.randint(100000, 999999))
    otp.created_at = timezone.now()
    otp.used = False  # Reset the 'used' flag when a new OTP is generated
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
    return otp.code


# || OTP VERIFICATIONS
class OTPVerificationView(View):
    def get(self, request):
        return render(request, "authentic/otp_verification.html")

    def post(self, request):
        otp_code = request.POST.get("otp_code")
        try:
            otp = OTP.objects.get(code=otp_code, used=False)
            if otp.is_valid():
                otp.used = True
                otp.save()

                user = otp.user
                user.is_active = True
                user.save()

                login(request, user)
                messages.success(request, "OTP verification successful.")

                # Get the redirect_url from the query parameters
                redirect_url = request.GET.get("redirect_url", "index")
                return redirect(redirect_url)
            else:
                messages.error(request, "Invalid OTP.\n Send new request")
                return redirect("otp_verification")

        except OTP.DoesNotExist:
            messages.error(request, "Invalid OTP")
            return redirect("otp_verification")


# Resend OTP CODE
def resend_otp(request):
    if request.method == "POST":  # Ensure it's a POST request
        user = request.user  # Get the currently logged-in user
        send_otp(
            user, "Your New OTP Code", "Your OTP code is {otp_code}.", [user.email]
        )
        messages.success(request, "A new OTP has been sent to your email.")
    else:
        messages.error(request, "Invalid request method.")

    return redirect("otp_verification")


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
    success_url = reverse_lazy("otp_verification")  # Default success URL

    def form_valid(self, form):
        user = form.save()
        if user:
            try:
                # Send OTP after successful registration
                send_otp(
                    user,
                    "Your OTP Code for Registering to Nutcracker",
                    "Hi,\nYour OTP code is: [{otp_code}].\n Valid for the next 5 minutes.\n Do not share this code with anyone",
                    [form.cleaned_data["email"]],
                )
                messages.success(self.request, "OTP has been sent to your email.")

                redirect_url = reverse("index")
                otp_url = f"{reverse('otp_verification')}?redirect_url={redirect_url}"
                return redirect(otp_url)

            except Exception as e:
                messages.error(self.request, "Connection required.")
                return redirect(self.request.META.get("HTTP_REFERER", "index"))

        # If user saving fails, fall back to default behavior
        return super().form_invalid(form)


class UserLoginView(FormView):
    template_name = "authentic/user_login.html"
    form_class = UserLoginForm

    def post(self, request, *args, **kwargs):
        uname = request.POST.get("username")
        psw = request.POST.get("password")
        user = authenticate(request, username=uname, password=psw)
        if user:
            login(request, user)
            try:
                # Send OTP
                send_otp(
                    user,
                    "Your OTP Code for Login",
                    "Hi,\nYour OTP code is: [{otp_code}].\n Valid for the next 5 minutes.\n Do not share this code with anyone",
                    [user.email],
                )
                messages.success(request, "OTP for verification is sent to your email")

                # Generate the redirect URL and pass it as a query parameter
                redirect_url = reverse("index")  # Reverse the URL for the 'index' view
                otp_verification_url = (
                    f"{reverse('otp_verification')}?redirect_url={redirect_url}"
                )

                return redirect(otp_verification_url)
            except Exception as e:
                messages.error(self.request, "Connection required.")
                return redirect(self.request.META.get("HTTP_REFERER", "index"))
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")

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


class ForgotPasswordView(FormView):
    template_name = "authentic/password_reset_request.html"
    form_class = ForgotPasswordForm

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        user = User.objects.filter(username=username, email=email).first()
        if user:
            try:
                # otp_code=send_otp(
                #     user,
                #     "Your OTP Code for Password Reset",
                #     "Hi,\nYour OTP code is: [{otp_code}]. Valid for the next 5 minutes.",
                #     [user.email],
                # )
                otp, created = OTP.objects.get_or_create(user=user)
                otp.code = str(random.randint(100000, 999999))
                otp.created_at = timezone.now()
                otp.used = False  # Reset the 'used' flag when a new OTP is generated
                otp.save()
                # messages.success(self.request, "OTP has been sent to your email.")
                # redirect_url = reverse('reset_password')
                # otp_url = f"{reverse('reset_password')}?otp_code={otp.code}&email={user.email}"
                otp_url = f"{reverse('reset_password')}?otp_code={otp.code}&email={user.email}&username={username}"
                # otp_url =f"{reverse('otp_verification')}?redirect_url={redirect_url}"
                return redirect(otp_url)
            except:
                messages.error(self.request, "Connection requeared.")
                return redirect(self.request.META.get("HTTP_REFERER", "index"))
        else:
            messages.error(self.request, "User with this email does not exist.")
            return redirect("login")


class ResetPasswordView(FormView):
    template_name = "authentic/reset_password.html"
    form_class = PasswordResetForm

    def dispatch(self, request, *args, **kwargs):
        self.otp_code = request.GET.get("otp_code")  # Get the OTP code from the URL
        self.user_email = request.GET.get("email")
        self.username = request.GET.get("username")
        # get the user instences
        self.user = User.objects.filter(
            username=self.username, email=self.user_email
        ).first()
        if not self.user:
            messages.error(request, "User not found.")
            return redirect("forgot_password")

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.user  # Pass the user instance to the form
        return kwargs

    def form_valid(self, form):
        otp = OTP.objects.filter(user=self.user, code=self.otp_code, used=False).first()
        if otp and otp.is_valid():
            self.user.set_password(
                form.cleaned_data["new_password1"]
            )  # Set the new password
            self.user.save()
            otp.used = True  # Mark the OTP as used
            otp.save()
            messages.success(self.request, "Your password has been reset successfully.")
            return redirect("login")  # Redirect to the login page
        else:
            messages.error(self.request, "Invalid or expired OTP.")
            return redirect("forgot_password")  # Redirect back to forgot password

    def form_invalid(self, form):
        return super().form_invalid(form)


# Profile Update view
@method_decorator(login_required, name="dispatch")
class ProfileFormView(FormView):
    template_name = "profile_view.html"
    form_class = ProfileForm

    def get_success_url(self):
        if 'checkout' in self.request.GET:
            return reverse_lazy('checkout')  # Redirect to checkout page
        return reverse_lazy('index')
    
    def get_form_kwargs(self):
        # Pass the request.user to the form for initializing first name, last name, and email
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_initial(self):
        # Initialize the form with data from the User model
        initial = super().get_initial()
        user = self.request.user
        initial["email"] = user.email
        initial["first_name"] = user.first_name
        initial["last_name"] = user.last_name

        # Get the profile instance if it exists and populate form with profile data
        try:
            profile = Profile.objects.get(user=user)
            initial["mobile_number"] = profile.mobile_number
            initial["address"] = profile.address
            initial["pin_code"] = profile.pin_code
        except Profile.DoesNotExist:
            # If profile doesn't exist
            pass
        return initial

    def form_valid(self, form):
        # Create or update the profile instance linked to the user
        profile, created = Profile.objects.get_or_create(user=self.request.user)

        # Update the profile fields with the form data
        profile.mobile_number = form.cleaned_data.get("mobile_number")
        profile.address = form.cleaned_data.get("address")
        profile.pin_code = form.cleaned_data.get("pin_code")

        # Save the profile
        profile.save()

        # Update the first_name and last_name in the User model
        self.request.user.first_name = form.cleaned_data.get("first_name")
        self.request.user.last_name = form.cleaned_data.get("last_name")
        self.request.user.save()

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
        if request.method == "POST":
            if request.POST.get("action") == "add_to_cart":
                user = request.user
                product = Products.objects.get(pk=kwargs.get("pk"))
                qty = int(
                    request.POST.get("quantity", 1)
                )  # Default to 1 if not provided

                # Check if the product is already in the cart
                cart_item, created = Cart.objects.get_or_create(
                    user=user,
                    product=product,
                    status="in-cart",
                    defaults={"quantity": qty},
                )

                if not created:
                    # If the cart item already exists, update the quantity
                    cart_item.quantity += qty
                    cart_item.save()
                    messages.success(
                        request, f"Updated qty of {product.title} in your cart."
                    )
                else:
                    messages.success(request, f"Added {product.title} to your cart.")

                return redirect("cart_list")
            elif request.POST.get("action") == "buy_now":

                return redirect("profile_update")


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
