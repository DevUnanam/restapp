from django import forms
from .models import Restaurant, MenuItem


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'address', 'phone_number', 'image', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-leafy-green focus:border-transparent',
                'placeholder': 'Restaurant Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-leafy-green focus:border-transparent',
                'placeholder': 'Describe your restaurant...',
                'rows': 4
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-leafy-green focus:border-transparent',
                'placeholder': 'Full Address',
                'rows': 3
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-leafy-green focus:border-transparent',
                'placeholder': '+1234567890'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-leafy-green focus:border-transparent'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-leafy-green focus:ring-leafy-green border-gray-300 rounded'
            }),
        }


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'category', 'image', 'is_available', 'is_chefs_special']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-leafy-green focus:border-transparent',
                'placeholder': 'Menu Item Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-leafy-green focus:border-transparent',
                'placeholder': 'Describe this dish...',
                'rows': 3
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-leafy-green focus:border-transparent',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'category': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-leafy-green focus:border-transparent',
                'placeholder': 'e.g., Appetizers, Main Course, Desserts'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-leafy-green focus:border-transparent'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-leafy-green focus:ring-leafy-green border-gray-300 rounded'
            }),
            'is_chefs_special': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-carrot-orange focus:ring-carrot-orange border-gray-300 rounded'
            }),
        }
