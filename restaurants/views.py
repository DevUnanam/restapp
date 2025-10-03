from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Restaurant, MenuItem
from .serializers import RestaurantSerializer, RestaurantListSerializer, MenuItemSerializer
from users.permissions import IsMerchant


# API Views
class RestaurantListCreateAPIView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RestaurantListSerializer
        return RestaurantSerializer

    def perform_create(self, serializer):
        serializer.save(merchant=self.request.user)


class RestaurantDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'merchant':
            return Restaurant.objects.filter(merchant=self.request.user)
        return Restaurant.objects.all()


class MenuItemListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return MenuItem.objects.filter(restaurant_id=restaurant_id)

    def perform_create(self, serializer):
        restaurant_id = self.kwargs.get('restaurant_id')
        restaurant = get_object_or_404(Restaurant, id=restaurant_id, merchant=self.request.user)
        serializer.save(restaurant=restaurant)


class MenuItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'merchant':
            return MenuItem.objects.filter(restaurant__merchant=self.request.user)
        return MenuItem.objects.all()
