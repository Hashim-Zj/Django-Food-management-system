from django.urls import path
from . import views

urlpatterns = [
  path('',views.AdminHomeView.as_view(),name='admin_index'),
  path('login',views.AdminLoginView.as_view(),name='admin_login'),
  path('logout',views.LogoutView.as_view(),name='admin_logout'),
  path('category/list&add',views.CategoryView.as_view(),name='category_list'),
  path('category/edit/<int:id>',views.CategoryUpdateView.as_view(),name='category_edit'),
  path('category/delete/<int:id>',views.CategoryDeleteView.as_view(),name='category_delete'),
  path('product/list',views.ProductView.as_view(),name='product_list'),
  path('product/add',views.AddProductView.as_view(),name='add_product'),
  path('product/edit/<int:pk>',views.ProductUpdateView.as_view(), name='edit_product'),
  path('product/delete/<int:pk>/',views.ProductDeleteView.as_view(), name='delete_product'),
  path('orders/new/list/',views.NewOrderListView.as_view(), name='new_orders'),
  path('orders/list/',views.OrderListView.as_view(), name='list_orders'),
  path('order/detail/<int:pk>/',views.OrderDetailView.as_view(), name='order_detail'),

]
