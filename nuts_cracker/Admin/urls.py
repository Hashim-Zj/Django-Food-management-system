from django.urls import path
from . import views

urlpatterns = [
  path('',views.AdminHomeView.as_view(),name='admin_index'),
  path('AdminLogin',views.AdminLoginView.as_view(),name='admin_login'),
  path('categoryView',views.CategoryView.as_view(),name='category_view'),
  path('catg_update/<int:id>',views.CategoryUpdateView.as_view(),name='catg_update_view'),
  path('catg_delete/<int:id>',views.CategoryDeleteView.as_view(),name='catg_delete_view'),
]
