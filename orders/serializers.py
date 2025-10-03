from rest_framework import serializers
from .models import Order, OrderItem
from restaurants.serializers import MenuItemSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_details = MenuItemSerializer(source='menu_item', read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ('id', 'subtotal')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    driver_name = serializers.CharField(source='driver.username', read_only=True, allow_null=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('id', 'customer', 'created_at', 'updated_at')


class OrderCreateSerializer(serializers.Serializer):
    restaurant_id = serializers.IntegerField()
    delivery_address = serializers.CharField()
    notes = serializers.CharField(required=False, allow_blank=True)
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must have at least one item")
        return value


class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)
