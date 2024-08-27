from django.urls import path
from . import views

urlpatterns = [
  path('',views.AdminHomeView.as_view(),name='admin_index'),
  path('AdminLogin',views.AdminLoginView.as_view(),name='admin_login'),
]
