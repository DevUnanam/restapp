from django.urls import path
from . import views

urlpatterns = [
    # API URLs
    path('api/', views.OrderListCreateAPIView.as_view(), name='api_order_list'),
    path('api/create/', views.create_order, name='api_order_create'),
    path('api/<int:pk>/', views.OrderDetailAPIView.as_view(), name='api_order_detail'),
    path('api/<int:pk>/status/', views.update_order_status, name='api_order_status'),
    path('api/<int:pk>/assign/', views.assign_driver, name='api_order_assign'),
]
