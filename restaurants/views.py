from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Restaurant, MenuItem, Review
from .serializers import RestaurantSerializer, RestaurantListSerializer, MenuItemSerializer, ReviewSerializer
from users.permissions import IsMerchant, IsCustomer


# API Views
class RestaurantListCreateAPIView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RestaurantListSerializer
        return RestaurantSerializer

    def perform_create(self, serializer):
        # Only merchants can create restaurants
        if self.request.user.role != 'merchant':
            raise PermissionDenied("Only merchants can create restaurants")
        serializer.save(merchant=self.request.user)


class RestaurantDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Merchants can only access their own restaurants
        if self.request.user.role == 'merchant':
            return Restaurant.objects.filter(merchant=self.request.user)
        return Restaurant.objects.all()

    def perform_update(self, serializer):
        # Only the merchant owner can update
        if self.request.user.role != 'merchant' or serializer.instance.merchant != self.request.user:
            raise PermissionDenied("You can only update your own restaurant")
        serializer.save()

    def perform_destroy(self, instance):
        # Only the merchant owner can delete
        if self.request.user.role != 'merchant' or instance.merchant != self.request.user:
            raise PermissionDenied("You can only delete your own restaurant")
        instance.delete()


class MenuItemListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return MenuItem.objects.filter(restaurant_id=restaurant_id)

    def perform_create(self, serializer):
        # Only the merchant owner can add menu items
        restaurant_id = self.kwargs.get('restaurant_id')
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        if self.request.user.role != 'merchant' or restaurant.merchant != self.request.user:
            raise PermissionDenied("You can only add menu items to your own restaurant")
        serializer.save(restaurant=restaurant)


class MenuItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'merchant':
            return MenuItem.objects.filter(restaurant__merchant=self.request.user)
        return MenuItem.objects.all()

    def perform_update(self, serializer):
        # Only the merchant owner can update
        if self.request.user.role != 'merchant' or serializer.instance.restaurant.merchant != self.request.user:
            raise PermissionDenied("You can only update menu items from your own restaurant")
        serializer.save()

    def perform_destroy(self, instance):
        # Only the merchant owner can delete
        if self.request.user.role != 'merchant' or instance.restaurant.merchant != self.request.user:
            raise PermissionDenied("You can only delete menu items from your own restaurant")
        instance.delete()


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Review.objects.filter(restaurant_id=restaurant_id)

    def perform_create(self, serializer):
        # Only customers can create reviews
        if self.request.user.role != 'customer':
            raise PermissionDenied("Only customers can leave reviews")
        restaurant_id = self.kwargs.get('restaurant_id')
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        serializer.save(customer=self.request.user, restaurant=restaurant)


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'customer':
            return Review.objects.filter(customer=self.request.user)
        return Review.objects.all()

    def perform_update(self, serializer):
        # Only the review owner can update
        if serializer.instance.customer != self.request.user:
            raise PermissionDenied("You can only update your own reviews")
        serializer.save()

    def perform_destroy(self, instance):
        # Only the review owner can delete
        if instance.customer != self.request.user:
            raise PermissionDenied("You can only delete your own reviews")
        instance.delete()
