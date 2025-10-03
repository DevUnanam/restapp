# Quick Start Guide

## Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database
```bash
python manage.py migrate
python manage.py seed_data
```

### 3. Run Server
```bash
python manage.py runserver
```

Visit **http://localhost:8000** and login with:
- Customer: `customer1` / `password123`
- Admin: `admin` / `admin123`

## What You Can Do

### As a Customer
1. Login at http://localhost:8000/login/
2. Browse restaurants on your dashboard
3. Click "View Menu" on any restaurant
4. Add items to cart and checkout
5. Track your order status

### As a Merchant
1. Login as `merchant1` / `password123`
2. View your restaurants and incoming orders
3. Use Django Admin to add/edit restaurants and menu items

### As a Driver
1. Login as `driver1` / `password123`
2. View assigned deliveries
3. Update delivery status

### As an Admin
1. Login as `admin` / `admin123`
2. View platform statistics
3. Assign drivers to pending orders
4. Access full Django admin panel

## Testing the API

### Get JWT Token
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"customer1","password":"password123"}'
```

### List Restaurants
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/restaurants/api/
```

### Create Order
```bash
curl -X POST http://localhost:8000/orders/api/create/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "restaurant_id": 1,
    "delivery_address": "123 Main St",
    "items": [{"menu_item_id": "1", "quantity": "2"}]
  }'
```

## Sample Data

After seeding, you have:
- **3 Restaurants**: Italian Bistro, Sushi Palace, Burger Haven
- **15 Menu Items**: 5 items per restaurant
- **3 Customers**, **3 Merchants**, **3 Drivers**
- **1 Sample Order**

## Key URLs

- **Login**: http://localhost:8000/login/
- **Register**: http://localhost:8000/register/
- **Customer Dashboard**: http://localhost:8000/dashboard/customer/
- **Django Admin**: http://localhost:8000/admin/

## Need Help?

- See [README.md](README.md) for full documentation
- See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details

## Tips

1. Use different browsers/incognito windows to test different user roles simultaneously
2. Check Django admin panel to manage all data visually
3. Order status updates automatically on customer dashboard every 10 seconds
4. The leafy green (#4CAF50) and carrot orange (#FF9800) theme is consistent across all pages

Enjoy building with FoodDelivery! 🍔🍕🍣
