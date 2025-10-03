from django.contrib import admin
from .models import Restaurant, MenuItem


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'merchant', 'address', 'is_active', 'rating', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'merchant__username', 'address')
    ordering = ('-created_at',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'category', 'is_available', 'created_at')
    list_filter = ('is_available', 'category', 'created_at')
    search_fields = ('name', 'restaurant__name', 'category')
    ordering = ('restaurant', 'category', 'name')
