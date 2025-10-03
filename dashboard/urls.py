from django.urls import path
from . import views

urlpatterns = [
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('merchant/', views.merchant_dashboard, name='merchant_dashboard'),
    path('driver/', views.driver_dashboard, name='driver_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
]
