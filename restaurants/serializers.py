from rest_framework import serializers
from .models import Restaurant, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class RestaurantSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)
    merchant_name = serializers.CharField(source='merchant.username', read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = ('id', 'merchant', 'rating', 'created_at', 'updated_at')


class RestaurantListSerializer(serializers.ModelSerializer):
    merchant_name = serializers.CharField(source='merchant.username', read_only=True)
    menu_items_count = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'description', 'address', 'phone_number', 'image', 'is_active', 'rating', 'merchant_name', 'menu_items_count')

    def get_menu_items_count(self, obj):
        return obj.menu_items.filter(is_available=True).count()
