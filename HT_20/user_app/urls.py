from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('purchase/', views.purchase, name='cart'),
    path('purchase/<int:pk>/', views.add_to_purchase, name='purchase'),
    path('product/<int:pk>/', views.product_info, name='product_info'),
    path('edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('delete/<int:pk>/', views.delete, name='delete_product'),
    path('category/<name>/', views.category, name='category')
]