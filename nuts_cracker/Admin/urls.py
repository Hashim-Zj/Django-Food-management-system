from django.urls import path
from . import views

urlpatterns = [
  path('',views.AdminHomeView.as_view(),name='admin_index'),
  path('AdminLogin',views.AdminLoginView.as_view(),name='admin_login'),
  path('AdminLogout',views.LogoutView.as_view(),name='admin_logout'),
  path('category/list&add',views.CategoryView.as_view(),name='category_list'),
  path('category/edit/<int:id>',views.CategoryUpdateView.as_view(),name='category_edit'),
  path('category/delete/<int:id>',views.CategoryDeleteView.as_view(),name='category_delete'),
  path('product/list',views.ProductView.as_view(),name='product_list'),
  path('product/add',views.AddProductView.as_view(),name='add_product'),
  path('product/edit/<int:pk>',views.ProductUpdateView.as_view(), name='edit_product'),
  path('product/delete/<int:pk>/',views.ProductDeleteView.as_view(), name='delete_product'),
]
