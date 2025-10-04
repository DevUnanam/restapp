from django.urls import path
from . import views

urlpatterns = [
    # API URLs
    path('api/', views.RestaurantListCreateAPIView.as_view(), name='api_restaurant_list_create'),
    path('api/<int:pk>/', views.RestaurantDetailAPIView.as_view(), name='api_restaurant_detail'),
    path('api/<int:restaurant_id>/menu/', views.MenuItemListCreateAPIView.as_view(), name='api_menu_list_create'),
    path('api/menu/<int:pk>/', views.MenuItemDetailAPIView.as_view(), name='api_menu_detail'),
    path('api/<int:restaurant_id>/reviews/', views.ReviewListCreateAPIView.as_view(), name='api_review_list_create'),
    path('api/reviews/<int:pk>/', views.ReviewDetailAPIView.as_view(), name='api_review_detail'),
]
