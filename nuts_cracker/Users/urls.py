from django.urls import path
from .import views

urlpatterns = [
  path('',views.MainDisplayView.as_view(), name='index'),
  path('auth/register/',views.UserRegisterView.as_view(), name='register'),
  path('auth/login/',views.UserLoginView.as_view(), name='login'),
  path('auth/logout/',views.UserLogoutView.as_view(), name='logout'),
  path('auth/password_reset_request/',views.PasswordResetRequestView.as_view(), name='psw_reset_request'),
  path('auth/otp-verification/',views.OTPVerificationView.as_view(), name='otp_verification'),
  path('auth/resend_otp/',views.resend_otp, name='otp_resend'),
  path('create-profile/',views.ProfileCreateView.as_view(), name='create_profile'),
  path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
  path('add_to_cart/<int:pk>/', views.AddToCartView.as_view(), name='add_to_cart'),
  path('cartlist/',views.CartListView.as_view(),name='cartlist'),
  path('wishlist/add/<int:pk>/', views.AddToWishlistView.as_view(), name='add_to_wishlist'),
  path('wishlist/',views.WishlistView.as_view(), name='wishlist'),
  path('wishlist/add/<int:pk>/', views.AddToWishlistView.as_view(), name='add_to_wishlist'),
  path('wishlist/remove/<int:pk>/',views.RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),

  # path('place_order/<int:pk>/', views.place_order, name='place_order'),
  path('non-existing-page/',views.non_existing_view, name='non_existing'),
]
