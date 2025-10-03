from django.contrib import admin
from .models import DriverProfile


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('driver', 'vehicle_type', 'vehicle_number', 'is_available', 'rating', 'total_deliveries')
    list_filter = ('is_available', 'vehicle_type')
    search_fields = ('driver__username', 'vehicle_number', 'license_number')
    ordering = ('-created_at',)
