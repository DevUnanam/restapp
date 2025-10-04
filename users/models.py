from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('driver', 'Driver'),
        ('merchant', 'Merchant'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class CustomerProfile(models.Model):
    customer = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'customer'},
        related_name='customer_profile'
    )
    delivery_address = models.TextField(blank=True, null=True)
    preferences = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.username} - Customer Profile"

    class Meta:
        db_table = 'customer_profiles'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create appropriate profile when user is created"""
    if created:
        if instance.role == 'customer':
            CustomerProfile.objects.get_or_create(customer=instance)
        elif instance.role == 'driver':
            # Import here to avoid circular import
            from delivery.models import DriverProfile
            DriverProfile.objects.get_or_create(
                driver=instance,
                defaults={
                    'vehicle_type': 'Not Specified',
                    'vehicle_number': 'TBD',
                    'license_number': 'TBD'
                }
            )
        elif instance.role == 'merchant':
            # Import here to avoid circular import
            from restaurants.models import Restaurant
            # Note: Restaurant creation is intentionally manual as it requires more details
