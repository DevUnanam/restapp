from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import User
from restaurants.models import Restaurant, MenuItem
from orders.models import Order
from delivery.models import DriverProfile


@login_required
def customer_dashboard(request):
    if request.user.role != 'customer':
        messages.error(request, 'Access denied')
        return redirect('dashboard')

    restaurants = Restaurant.objects.filter(is_active=True)
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')

    context = {
        'restaurants': restaurants,
        'orders': orders,
    }
    return render(request, 'dashboard/customer_dashboard.html', context)


@login_required
def merchant_dashboard(request):
    if request.user.role != 'merchant':
        messages.error(request, 'Access denied')
        return redirect('dashboard')

    restaurants = Restaurant.objects.filter(merchant=request.user)
    orders = Order.objects.filter(restaurant__merchant=request.user).order_by('-created_at')

    context = {
        'restaurants': restaurants,
        'orders': orders,
    }
    return render(request, 'dashboard/merchant_dashboard.html', context)


@login_required
def driver_dashboard(request):
    if request.user.role != 'driver':
        messages.error(request, 'Access denied')
        return redirect('dashboard')

    orders = Order.objects.filter(driver=request.user).order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'dashboard/driver_dashboard.html', context)


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied')
        return redirect('dashboard')

    total_users = User.objects.count()
    total_customers = User.objects.filter(role='customer').count()
    total_merchants = User.objects.filter(role='merchant').count()
    total_drivers = User.objects.filter(role='driver').count()
    total_restaurants = Restaurant.objects.count()
    total_orders = Order.objects.count()

    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    recent_restaurants = Restaurant.objects.all().order_by('-created_at')[:10]

    context = {
        'total_users': total_users,
        'total_customers': total_customers,
        'total_merchants': total_merchants,
        'total_drivers': total_drivers,
        'total_restaurants': total_restaurants,
        'total_orders': total_orders,
        'recent_orders': recent_orders,
        'recent_restaurants': recent_restaurants,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    menu_items = MenuItem.objects.filter(restaurant=restaurant, is_available=True)

    context = {
        'restaurant': restaurant,
        'menu_items': menu_items,
    }
    return render(request, 'dashboard/restaurant_detail.html', context)
