from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from restaurants.models import Restaurant, MenuItem
from orders.models import Order, OrderItem
from delivery.models import DriverProfile
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Create admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@fooddelivery.com',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'is_verified': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Create customers
        customers = []
        for i in range(1, 4):
            customer, created = User.objects.get_or_create(
                username=f'customer{i}',
                defaults={
                    'email': f'customer{i}@example.com',
                    'role': 'customer',
                    'phone_number': f'+1234567890{i}',
                    'address': f'{i}23 Main St, City, State',
                    'is_verified': True
                }
            )
            if created:
                customer.set_password('password123')
                customer.save()
                self.stdout.write(self.style.SUCCESS(f'Created customer{i}'))
            customers.append(customer)

        # Create merchants
        merchants = []
        merchant_names = ['Italian Bistro', 'Sushi Palace', 'Burger Haven']
        for i, name in enumerate(merchant_names, 1):
            merchant, created = User.objects.get_or_create(
                username=f'merchant{i}',
                defaults={
                    'email': f'merchant{i}@example.com',
                    'role': 'merchant',
                    'phone_number': f'+1987654320{i}',
                    'address': f'{i}00 Business Ave, City, State',
                    'is_verified': True
                }
            )
            if created:
                merchant.set_password('password123')
                merchant.save()
                self.stdout.write(self.style.SUCCESS(f'Created merchant{i}'))
            merchants.append(merchant)

        # Create drivers
        drivers = []
        for i in range(1, 4):
            driver, created = User.objects.get_or_create(
                username=f'driver{i}',
                defaults={
                    'email': f'driver{i}@example.com',
                    'role': 'driver',
                    'phone_number': f'+1555123450{i}',
                    'address': f'{i}50 Driver Lane, City, State',
                    'is_verified': True
                }
            )
            if created:
                driver.set_password('password123')
                driver.save()
                self.stdout.write(self.style.SUCCESS(f'Created driver{i}'))

                # Create driver profile
                DriverProfile.objects.get_or_create(
                    driver=driver,
                    defaults={
                        'vehicle_type': 'Motorcycle' if i == 1 else 'Car',
                        'vehicle_number': f'ABC-{i}23',
                        'license_number': f'DL{i}234567',
                        'is_available': True,
                        'rating': Decimal('4.5')
                    }
                )
                self.stdout.write(self.style.SUCCESS(f'Created driver profile for driver{i}'))
            drivers.append(driver)

        # Create restaurants and menu items
        restaurants_data = [
            {
                'merchant': merchants[0],
                'name': 'Italian Bistro',
                'description': 'Authentic Italian cuisine with fresh pasta and wood-fired pizzas',
                'address': '100 Business Ave, City, State',
                'phone_number': '+19876543201',
                'rating': Decimal('4.7'),
                'menu_items': [
                    {'name': 'Margherita Pizza', 'description': 'Fresh tomatoes, mozzarella, basil', 'price': Decimal('12.99'), 'category': 'Pizza'},
                    {'name': 'Spaghetti Carbonara', 'description': 'Classic Roman pasta dish', 'price': Decimal('14.99'), 'category': 'Pasta'},
                    {'name': 'Lasagna', 'description': 'Layered pasta with meat sauce and cheese', 'price': Decimal('15.99'), 'category': 'Pasta'},
                    {'name': 'Caesar Salad', 'description': 'Romaine lettuce, parmesan, croutons', 'price': Decimal('8.99'), 'category': 'Salads'},
                    {'name': 'Tiramisu', 'description': 'Classic Italian dessert', 'price': Decimal('6.99'), 'category': 'Desserts'},
                ]
            },
            {
                'merchant': merchants[1],
                'name': 'Sushi Palace',
                'description': 'Fresh sushi and Japanese delicacies',
                'address': '200 Business Ave, City, State',
                'phone_number': '+19876543202',
                'rating': Decimal('4.8'),
                'menu_items': [
                    {'name': 'California Roll', 'description': 'Crab, avocado, cucumber', 'price': Decimal('9.99'), 'category': 'Rolls'},
                    {'name': 'Salmon Nigiri', 'description': 'Fresh salmon on rice', 'price': Decimal('5.99'), 'category': 'Nigiri'},
                    {'name': 'Spicy Tuna Roll', 'description': 'Tuna with spicy mayo', 'price': Decimal('11.99'), 'category': 'Rolls'},
                    {'name': 'Miso Soup', 'description': 'Traditional Japanese soup', 'price': Decimal('3.99'), 'category': 'Soups'},
                    {'name': 'Edamame', 'description': 'Steamed soybeans', 'price': Decimal('4.99'), 'category': 'Appetizers'},
                ]
            },
            {
                'merchant': merchants[2],
                'name': 'Burger Haven',
                'description': 'Gourmet burgers and comfort food',
                'address': '300 Business Ave, City, State',
                'phone_number': '+19876543203',
                'rating': Decimal('4.5'),
                'menu_items': [
                    {'name': 'Classic Cheeseburger', 'description': 'Beef patty with cheese, lettuce, tomato', 'price': Decimal('10.99'), 'category': 'Burgers'},
                    {'name': 'Bacon Burger', 'description': 'Beef patty with bacon and cheese', 'price': Decimal('12.99'), 'category': 'Burgers'},
                    {'name': 'Veggie Burger', 'description': 'Plant-based patty with toppings', 'price': Decimal('11.99'), 'category': 'Burgers'},
                    {'name': 'French Fries', 'description': 'Crispy golden fries', 'price': Decimal('4.99'), 'category': 'Sides'},
                    {'name': 'Milkshake', 'description': 'Vanilla, chocolate, or strawberry', 'price': Decimal('5.99'), 'category': 'Drinks'},
                ]
            }
        ]

        for restaurant_data in restaurants_data:
            menu_items_data = restaurant_data.pop('menu_items')
            restaurant, created = Restaurant.objects.get_or_create(
                name=restaurant_data['name'],
                merchant=restaurant_data['merchant'],
                defaults=restaurant_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created restaurant: {restaurant.name}'))

            # Create menu items
            for item_data in menu_items_data:
                menu_item, created = MenuItem.objects.get_or_create(
                    restaurant=restaurant,
                    name=item_data['name'],
                    defaults=item_data
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  - Created menu item: {menu_item.name}'))

        # Create sample orders
        restaurants = Restaurant.objects.all()
        if restaurants.exists() and customers:
            restaurant = restaurants.first()
            menu_items = restaurant.menu_items.all()[:2]

            if menu_items:
                total = sum(item.price * 2 for item in menu_items)
                order, created = Order.objects.get_or_create(
                    customer=customers[0],
                    restaurant=restaurant,
                    defaults={
                        'delivery_address': customers[0].address,
                        'total_amount': total,
                        'status': 'pending',
                        'notes': 'Please ring the doorbell'
                    }
                )

                if created:
                    for item in menu_items:
                        OrderItem.objects.create(
                            order=order,
                            menu_item=item,
                            quantity=2,
                            price=item.price,
                            subtotal=item.price * 2
                        )
                    self.stdout.write(self.style.SUCCESS(f'Created sample order #{order.id}'))

        self.stdout.write(self.style.SUCCESS('\nDatabase seeding completed!'))
        self.stdout.write(self.style.WARNING('\nLogin credentials:'))
        self.stdout.write('Admin: username=admin, password=admin123')
        self.stdout.write('Customer: username=customer1, password=password123')
        self.stdout.write('Merchant: username=merchant1, password=password123')
        self.stdout.write('Driver: username=driver1, password=password123')
