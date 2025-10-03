from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import User
from .serializers import UserSerializer, UserProfileSerializer


# API Views
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)


# Template Views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'users/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        role = request.POST.get('role', 'customer')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')

        if password != password2:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
                phone_number=phone_number,
                address=address
            )
            login(request, user)
            return redirect('dashboard')

    return render(request, 'users/register.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    user = request.user

    # Redirect to appropriate dashboard based on role
    if user.role == 'customer':
        return redirect('customer_dashboard')
    elif user.role == 'merchant':
        return redirect('merchant_dashboard')
    elif user.role == 'driver':
        return redirect('driver_dashboard')
    elif user.role == 'admin':
        return redirect('admin_dashboard')
    else:
        return redirect('login')
