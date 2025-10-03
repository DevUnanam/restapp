# Testing Guide

## Manual Testing Checklist

### Initial Setup
```bash
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

---

## Test Case 1: Customer Journey (End-to-End)

### Step 1: Registration
1. Go to http://localhost:8000/register/
2. Fill in the form:
   - Username: `testcustomer`
   - Email: `test@example.com`
   - Role: Customer
   - Phone: `+1234567890`
   - Address: `123 Test St`
   - Password: `testpass123`
3. ✅ **Expected**: Redirected to customer dashboard

### Step 2: Browse Restaurants
1. On customer dashboard
2. ✅ **Expected**: See 3 restaurants (Italian Bistro, Sushi Palace, Burger Haven)
3. ✅ **Expected**: Each shows rating, address, and "View Menu" button

### Step 3: View Menu
1. Click "View Menu" on Italian Bistro
2. ✅ **Expected**: See 5 menu items with prices
3. ✅ **Expected**: Categories shown (Pizza, Pasta, Salads, Desserts)

### Step 4: Place Order
1. Click "Add to Cart" on Margherita Pizza (2x)
2. Click "Add to Cart" on Spaghetti Carbonara (1x)
3. ✅ **Expected**: Cart appears at bottom showing "3 items"
4. Click "Checkout"
5. ✅ **Expected**: Modal opens with cart details
6. Enter delivery address
7. Click "Place Order"
8. ✅ **Expected**: Success message and redirect to dashboard

### Step 5: Track Order
1. On customer dashboard, scroll to "Recent Orders"
2. ✅ **Expected**: See new order with status "Pending"
3. Wait 10 seconds
4. ✅ **Expected**: Status auto-updates (if admin assigned driver)

---

## Test Case 2: Admin Workflow

### Step 1: Login as Admin
1. Logout if logged in
2. Go to http://localhost:8000/login/
3. Login: `admin` / `admin123`
4. ✅ **Expected**: Redirected to admin dashboard

### Step 2: View Statistics
1. On admin dashboard
2. ✅ **Expected**: See statistics:
   - Total Users
   - Customers count
   - Merchants count
   - Drivers count
   - Restaurants count
   - Total Orders

### Step 3: Assign Driver to Order
1. Scroll to "Recent Orders"
2. Find order with status "Pending" and no driver
3. Click "Assign Driver"
4. ✅ **Expected**: Modal opens with driver list
5. Click on a driver
6. ✅ **Expected**: Driver assigned successfully
7. ✅ **Expected**: Order status updated to "Accepted"

### Step 4: Access Django Admin
1. Click "Django Admin" in navbar
2. ✅ **Expected**: Django admin panel opens
3. Click on "Restaurants"
4. ✅ **Expected**: See all restaurants
5. Click on "Users"
6. ✅ **Expected**: See all users with roles

---

## Test Case 3: Driver Workflow

### Step 1: Login as Driver
1. Logout
2. Login: `driver1` / `password123`
3. ✅ **Expected**: Redirected to driver dashboard

### Step 2: View Assigned Deliveries
1. On driver dashboard
2. ✅ **Expected**: See assigned orders (if any)
3. ✅ **Expected**: Each order shows:
   - Customer name and phone
   - Delivery address
   - Order items
   - Total amount
   - Current status

### Step 3: Update Delivery Status
1. Find order with status "Accepted"
2. Click "Start Delivery"
3. ✅ **Expected**: Status changes to "In Transit"
4. Click "Mark as Delivered"
5. ✅ **Expected**: Status changes to "Delivered"
6. ✅ **Expected**: Button changes to "✓ Delivered"

### Step 4: Auto-Refresh
1. Wait 30 seconds
2. ✅ **Expected**: Page auto-refreshes for new assignments

---

## Test Case 4: Merchant Workflow

### Step 1: Login as Merchant
1. Logout
2. Login: `merchant1` / `password123`
3. ✅ **Expected**: Redirected to merchant dashboard

### Step 2: View Restaurants
1. On merchant dashboard
2. ✅ **Expected**: See owned restaurant (Italian Bistro)
3. ✅ **Expected**: Shows rating, status (Active/Inactive), menu items count

### Step 3: View Incoming Orders
1. Scroll to "Incoming Orders"
2. ✅ **Expected**: See orders for this restaurant
3. ✅ **Expected**: Shows customer, items count, amount, status

### Step 4: Manage Restaurant (Django Admin)
1. Open new tab: http://localhost:8000/admin/
2. Login as admin
3. Navigate to Restaurants → Restaurants
4. Click on Italian Bistro
5. Add a new menu item:
   - Name: `Ravioli`
   - Description: `Cheese-filled pasta`
   - Price: `13.99`
   - Category: `Pasta`
   - Is available: ✓
6. Save
7. ✅ **Expected**: New item saved successfully

---

## Test Case 5: API Testing

### Setup: Get JWT Token
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"customer1","password":"password123"}'
```
✅ **Expected**: Returns `access` and `refresh` tokens

### Test 1: List Restaurants
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/restaurants/api/
```
✅ **Expected**: Returns JSON array of restaurants

### Test 2: Get Restaurant Details
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/restaurants/api/1/
```
✅ **Expected**: Returns restaurant with menu items

### Test 3: Create Order
```bash
curl -X POST http://localhost:8000/orders/api/create/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "restaurant_id": 1,
    "delivery_address": "456 Test Ave",
    "notes": "Ring doorbell",
    "items": [
      {"menu_item_id": "1", "quantity": "2"},
      {"menu_item_id": "2", "quantity": "1"}
    ]
  }'
```
✅ **Expected**: Returns created order with status 201

### Test 4: Get Orders
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/orders/api/
```
✅ **Expected**: Returns customer's orders

### Test 5: Invalid Token
```bash
curl -H "Authorization: Bearer INVALID_TOKEN" \
  http://localhost:8000/orders/api/
```
✅ **Expected**: Returns 401 Unauthorized

---

## Test Case 6: Role-Based Access Control

### Test 1: Customer Cannot Access Merchant API
1. Login as customer, get token
2. Try to create restaurant:
```bash
curl -X POST http://localhost:8000/restaurants/api/ \
  -H "Authorization: Bearer CUSTOMER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Restaurant",
    "description": "Test",
    "address": "123 Test",
    "phone_number": "123456"
  }'
```
✅ **Expected**: Returns 403 Forbidden (customer can't create restaurants)

### Test 2: Driver Cannot Access Customer Orders
1. Login as driver, get token
2. Try to create order:
```bash
curl -X POST http://localhost:8000/orders/api/create/ \
  -H "Authorization: Bearer DRIVER_TOKEN" \
  -d '{...}'
```
✅ **Expected**: Returns 403 Forbidden

### Test 3: Customer Cannot Update Others' Orders
1. Login as customer1
2. Create an order (note the order ID)
3. Login as customer2
4. Try to access customer1's order
✅ **Expected**: Order not visible in list

---

## Test Case 7: Frontend Interactions

### Test 1: Shopping Cart
1. Login as customer
2. Go to restaurant detail page
3. Add item to cart
4. ✅ **Expected**: Cart badge appears at bottom
5. Add another item
6. ✅ **Expected**: Cart count increases
7. Click cart
8. ✅ **Expected**: Modal shows all items
9. Change quantity
10. ✅ **Expected**: Subtotal updates
11. Remove item
12. ✅ **Expected**: Item removed from cart

### Test 2: Order Status Auto-Update
1. Login as customer with existing order
2. On dashboard, note current order status
3. In another browser/incognito:
   - Login as driver
   - Update the order status
4. Back to customer browser
5. Wait 10 seconds
6. ✅ **Expected**: Status badge updates without refresh

### Test 3: Responsive Design
1. Resize browser to mobile width (375px)
2. ✅ **Expected**: Navigation collapses properly
3. ✅ **Expected**: Restaurant grid becomes single column
4. ✅ **Expected**: Tables are scrollable
5. ✅ **Expected**: Modals fit screen

---

## Test Case 8: Error Handling

### Test 1: Empty Cart Checkout
1. Go to restaurant detail
2. Click "Checkout" without adding items
✅ **Expected**: "Your cart is empty" message

### Test 2: Missing Delivery Address
1. Add items to cart
2. Click checkout
3. Clear delivery address
4. Click "Place Order"
✅ **Expected**: "Please enter a delivery address" message

### Test 3: Invalid Login
1. Go to login page
2. Enter wrong password
✅ **Expected**: "Invalid username or password" message

### Test 4: Duplicate Username
1. Go to register page
2. Use existing username (`customer1`)
✅ **Expected**: "Username already exists" message

### Test 5: Password Mismatch
1. Go to register page
2. Enter different passwords in password fields
✅ **Expected**: "Passwords do not match" message

---

## Test Case 9: Database Integrity

### Test 1: Order Calculation
1. Create order with:
   - 2x Margherita Pizza ($12.99 each)
   - 1x Spaghetti Carbonara ($14.99)
2. ✅ **Expected**: Total = $40.97

### Test 2: Driver Assignment
1. Assign driver to order
2. ✅ **Expected**: Driver field populated
3. ✅ **Expected**: Driver can see order in their dashboard
4. ✅ **Expected**: Other drivers don't see this order

---

## Performance Tests

### Test 1: Page Load Time
1. Clear browser cache
2. Load customer dashboard
3. ✅ **Expected**: Page loads in < 2 seconds

### Test 2: API Response Time
```bash
time curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/restaurants/api/
```
✅ **Expected**: Response in < 500ms

### Test 3: Image Loading
1. Add images to restaurants
2. Reload page
3. ✅ **Expected**: Images load progressively
4. ✅ **Expected**: No broken image icons

---

## Security Tests

### Test 1: CSRF Protection
1. Try to submit login form without CSRF token
✅ **Expected**: Request rejected

### Test 2: SQL Injection
1. Try login with: `admin' OR '1'='1`
✅ **Expected**: Login fails, no SQL error

### Test 3: XSS Prevention
1. Create order with notes: `<script>alert('XSS')</script>`
✅ **Expected**: Script not executed, text escaped

---

## Browser Compatibility

Test in:
- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)

All features should work identically.

---

## Regression Testing Checklist

After any code changes, test:
- [ ] Login/Logout
- [ ] Registration
- [ ] Browse restaurants
- [ ] View menu
- [ ] Place order
- [ ] Driver status update
- [ ] Admin driver assignment
- [ ] API token generation
- [ ] Role-based access
- [ ] Cart functionality

---

## Known Limitations

1. Images not uploaded by default (use Django Admin to add)
2. No payment processing (dummy checkout)
3. No email notifications
4. Manual driver assignment (no automatic)
5. No real-time WebSocket updates (polling only)

These are intentional for this MVP version.

---

## Automated Testing (Future)

To add unit tests:
```python
# users/tests.py
from django.test import TestCase
from .models import User

class UserModelTest(TestCase):
    def test_create_customer(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpass',
            role='customer'
        )
        self.assertEqual(user.role, 'customer')
        self.assertFalse(user.is_verified)
```

Run with:
```bash
python manage.py test
```

---

## Bug Reporting

If you find any issues during testing:

1. Note the steps to reproduce
2. Screenshot the error (if visual)
3. Check browser console for JavaScript errors
4. Check Django server console for backend errors
5. Note your environment (OS, browser, Python version)

---

## Success Criteria

All test cases should pass for the application to be considered fully functional and ready for deployment.

✅ **Current Status**: All core features tested and working
