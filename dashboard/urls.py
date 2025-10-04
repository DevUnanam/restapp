from django.urls import path
from . import views

urlpatterns = [
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('merchant/', views.merchant_dashboard, name='merchant_dashboard'),
    path('driver/', views.driver_dashboard, name='driver_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),

    # Restaurant Management (specific paths before dynamic ones)
    path('restaurant/create/', views.create_restaurant, name='create_restaurant'),
    path('restaurant/<int:pk>/edit/', views.edit_restaurant, name='edit_restaurant'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),

    # Menu Management
    path('restaurant/<int:restaurant_id>/menu/', views.manage_menu, name='manage_menu'),
    path('restaurant/<int:restaurant_id>/menu/add/', views.add_menu_item, name='add_menu_item'),
    path('menu-item/<int:pk>/edit/', views.edit_menu_item, name='edit_menu_item'),
    path('menu-item/<int:pk>/delete/', views.delete_menu_item, name='delete_menu_item'),
]
