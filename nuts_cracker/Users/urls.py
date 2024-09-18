from django.urls import path
from .import views

urlpatterns = [
  path('',views.MainDisplayView.as_view(), name='index'),
  path('register/',views.UserRegisterView.as_view(), name='register'),
  path('otp-verification/',views.OTPVerificationView.as_view(), name='otp_verification'),
  path('login/',views.UserLoginView.as_view(), name='login'),
  path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
  path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
  path('place_order/<int:pk>/', views.place_order, name='place_order'),
]
