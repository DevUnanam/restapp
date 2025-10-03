from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer
from restaurants.models import Restaurant, MenuItem
from users.permissions import IsCustomer, IsDriver, IsMerchant


# API Views
class OrderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Order.objects.filter(customer=user)
        elif user.role == 'merchant':
            return Order.objects.filter(restaurant__merchant=user)
        elif user.role == 'driver':
            return Order.objects.filter(driver=user)
        elif user.role == 'admin':
            return Order.objects.all()
        return Order.objects.none()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    serializer = OrderCreateSerializer(data=request.data)

    if serializer.is_valid():
        restaurant_id = serializer.validated_data['restaurant_id']
        delivery_address = serializer.validated_data['delivery_address']
        notes = serializer.validated_data.get('notes', '')
        items_data = serializer.validated_data['items']

        restaurant = get_object_or_404(Restaurant, id=restaurant_id, is_active=True)

        # Calculate total amount
        total_amount = 0
        order_items = []

        for item_data in items_data:
            menu_item_id = int(item_data['menu_item_id'])
            quantity = int(item_data['quantity'])

            menu_item = get_object_or_404(MenuItem, id=menu_item_id, restaurant=restaurant, is_available=True)

            subtotal = menu_item.price * quantity
            total_amount += subtotal

            order_items.append({
                'menu_item': menu_item,
                'quantity': quantity,
                'price': menu_item.price,
                'subtotal': subtotal
            })

        # Create order
        order = Order.objects.create(
            customer=request.user,
            restaurant=restaurant,
            delivery_address=delivery_address,
            total_amount=total_amount,
            notes=notes
        )

        # Create order items
        for item in order_items:
            OrderItem.objects.create(
                order=order,
                menu_item=item['menu_item'],
                quantity=item['quantity'],
                price=item['price'],
                subtotal=item['subtotal']
            )

        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Order.objects.filter(customer=user)
        elif user.role == 'merchant':
            return Order.objects.filter(restaurant__merchant=user)
        elif user.role == 'driver':
            return Order.objects.filter(driver=user)
        elif user.role == 'admin':
            return Order.objects.all()
        return Order.objects.none()


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)

    # Check permissions
    user = request.user
    if user.role == 'driver' and order.driver != user:
        return Response({'error': 'You are not assigned to this order'}, status=status.HTTP_403_FORBIDDEN)
    elif user.role == 'merchant' and order.restaurant.merchant != user:
        return Response({'error': 'This order does not belong to your restaurant'}, status=status.HTTP_403_FORBIDDEN)
    elif user.role == 'customer':
        return Response({'error': 'Customers cannot update order status'}, status=status.HTTP_403_FORBIDDEN)

    serializer = OrderStatusUpdateSerializer(data=request.data)
    if serializer.is_valid():
        order.status = serializer.validated_data['status']
        order.save()
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def assign_driver(request, pk):
    if request.user.role != 'admin':
        return Response({'error': 'Only admins can assign drivers'}, status=status.HTTP_403_FORBIDDEN)

    order = get_object_or_404(Order, pk=pk)
    driver_id = request.data.get('driver_id')

    if not driver_id:
        return Response({'error': 'driver_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    from users.models import User
    driver = get_object_or_404(User, id=driver_id, role='driver')

    order.driver = driver
    order.save()

    serializer = OrderSerializer(order)
    return Response(serializer.data)
