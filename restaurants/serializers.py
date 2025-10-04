from rest_framework import serializers
from .models import Restaurant, MenuItem, Review


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'restaurant')


class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'restaurant', 'customer', 'customer_name', 'rating', 'comment', 'created_at', 'updated_at')
        read_only_fields = ('id', 'customer', 'created_at', 'updated_at')


class RestaurantSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)
    chefs_special = serializers.SerializerMethodField()
    merchant_name = serializers.CharField(source='merchant.username', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = ('id', 'merchant', 'rating', 'created_at', 'updated_at')

    def get_chefs_special(self, obj):
        special = obj.menu_items.filter(is_chefs_special=True, is_available=True).first()
        return MenuItemSerializer(special).data if special else None

    def get_reviews_count(self, obj):
        return obj.reviews.count()


class RestaurantListSerializer(serializers.ModelSerializer):
    merchant_name = serializers.CharField(source='merchant.username', read_only=True)
    menu_items_count = serializers.SerializerMethodField()
    chefs_special = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'description', 'address', 'phone_number', 'image', 'is_active', 'rating', 'merchant_name', 'menu_items_count', 'chefs_special')

    def get_menu_items_count(self, obj):
        return obj.menu_items.filter(is_available=True).count()

    def get_chefs_special(self, obj):
        special = obj.menu_items.filter(is_chefs_special=True, is_available=True).first()
        return MenuItemSerializer(special).data if special else None
