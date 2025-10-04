from django.contrib import admin
from .models import Restaurant, MenuItem, Review


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'merchant', 'address', 'is_active', 'rating', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'merchant__username', 'address')
    ordering = ('-created_at',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'category', 'is_available', 'is_chefs_special', 'created_at')
    list_filter = ('is_available', 'is_chefs_special', 'category', 'created_at')
    search_fields = ('name', 'restaurant__name', 'category')
    ordering = ('restaurant', 'category', 'name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'customer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('restaurant__name', 'customer__username', 'comment')
    ordering = ('-created_at',)
