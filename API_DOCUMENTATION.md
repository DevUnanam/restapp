# Food Delivery API Documentation

## Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_token>
```

### Authentication Endpoints

#### 1. Register User
- **URL**: `/api/register/`
- **Method**: `POST`
- **Auth Required**: No
- **Body**:
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "role": "customer|merchant|driver",
  "phone_number": "string (optional)",
  "address": "string (optional)"
}
```
- **Success Response**: `201 CREATED`
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "role": "customer",
  "phone_number": "+1234567890",
  "address": "123 Main St",
  "is_verified": false,
  "created_at": "2025-01-15T10:30:00Z"
}
```

#### 2. Login (Obtain Token)
- **URL**: `/api/token/`
- **Method**: `POST`
- **Auth Required**: No
- **Body**:
```json
{
  "username": "string",
  "password": "string"
}
```
- **Success Response**: `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 3. Refresh Token
- **URL**: `/api/token/refresh/`
- **Method**: `POST`
- **Auth Required**: No
- **Body**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 4. Get Current User
- **URL**: `/api/me/`
- **Method**: `GET`
- **Auth Required**: Yes

#### 5. Update Profile
- **URL**: `/api/profile/`
- **Method**: `GET`, `PUT`, `PATCH`
- **Auth Required**: Yes

---

## Restaurants API

### Restaurant Endpoints

#### 1. List Restaurants
- **URL**: `/restaurants/api/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
```json
[
  {
    "id": 1,
    "name": "Italian Bistro",
    "description": "Authentic Italian cuisine",
    "address": "100 Business Ave",
    "phone_number": "+1987654321",
    "image": "/media/restaurants/bistro.jpg",
    "is_active": true,
    "rating": "4.70",
    "merchant_name": "merchant1",
    "menu_items_count": 5
  }
]
```

#### 2. Create Restaurant (Merchant Only)
- **URL**: `/restaurants/api/`
- **Method**: `POST`
- **Auth Required**: Yes (Merchant role)
- **Body**:
```json
{
  "name": "string",
  "description": "string",
  "address": "string",
  "phone_number": "string",
  "image": "file (optional)"
}
```

#### 3. Get Restaurant Details
- **URL**: `/restaurants/api/{id}/`
- **Method**: `GET`
- **Auth Required**: Yes

#### 4. Update Restaurant
- **URL**: `/restaurants/api/{id}/`
- **Method**: `PUT`, `PATCH`
- **Auth Required**: Yes (Owner/Admin)

#### 5. Delete Restaurant
- **URL**: `/restaurants/api/{id}/`
- **Method**: `DELETE`
- **Auth Required**: Yes (Owner/Admin)

### Menu Items Endpoints

#### 1. List Menu Items
- **URL**: `/restaurants/api/{restaurant_id}/menu/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
```json
[
  {
    "id": 1,
    "restaurant": 1,
    "name": "Margherita Pizza",
    "description": "Fresh tomatoes, mozzarella, basil",
    "price": "12.99",
    "image": "/media/menu_items/pizza.jpg",
    "is_available": true,
    "category": "Pizza",
    "created_at": "2025-01-15T10:30:00Z"
  }
]
```

#### 2. Create Menu Item (Merchant Only)
- **URL**: `/restaurants/api/{restaurant_id}/menu/`
- **Method**: `POST`
- **Auth Required**: Yes (Merchant - Owner)
- **Body**:
```json
{
  "name": "string",
  "description": "string",
  "price": "decimal",
  "category": "string (optional)",
  "image": "file (optional)",
  "is_available": true
}
```

#### 3. Get Menu Item Details
- **URL**: `/restaurants/api/menu/{id}/`
- **Method**: `GET`
- **Auth Required**: Yes

#### 4. Update Menu Item
- **URL**: `/restaurants/api/menu/{id}/`
- **Method**: `PUT`, `PATCH`
- **Auth Required**: Yes (Owner/Admin)

#### 5. Delete Menu Item
- **URL**: `/restaurants/api/menu/{id}/`
- **Method**: `DELETE`
- **Auth Required**: Yes (Owner/Admin)

---

## Orders API

### Order Endpoints

#### 1. List Orders
- **URL**: `/orders/api/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Description**: Returns orders based on user role:
  - Customer: Their own orders
  - Merchant: Orders for their restaurants
  - Driver: Orders assigned to them
  - Admin: All orders
- **Success Response**: `200 OK`
```json
[
  {
    "id": 1,
    "customer": 2,
    "customer_name": "customer1",
    "restaurant": 1,
    "restaurant_name": "Italian Bistro",
    "driver": 3,
    "driver_name": "driver1",
    "status": "pending",
    "delivery_address": "123 Main St",
    "total_amount": "25.98",
    "notes": "Ring doorbell",
    "created_at": "2025-01-15T10:30:00Z",
    "items": [
      {
        "id": 1,
        "menu_item": 1,
        "menu_item_details": {...},
        "quantity": 2,
        "price": "12.99",
        "subtotal": "25.98"
      }
    ]
  }
]
```

#### 2. Create Order (Customer Only)
- **URL**: `/orders/api/create/`
- **Method**: `POST`
- **Auth Required**: Yes (Customer role)
- **Body**:
```json
{
  "restaurant_id": 1,
  "delivery_address": "123 Main St, City, State",
  "notes": "Optional notes",
  "items": [
    {
      "menu_item_id": "1",
      "quantity": "2"
    },
    {
      "menu_item_id": "3",
      "quantity": "1"
    }
  ]
}
```
- **Success Response**: `201 CREATED`

#### 3. Get Order Details
- **URL**: `/orders/api/{id}/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Permissions**: Customer (own orders), Merchant (restaurant orders), Driver (assigned orders), Admin (all)

#### 4. Update Order Status
- **URL**: `/orders/api/{id}/status/`
- **Method**: `PATCH`
- **Auth Required**: Yes (Driver/Merchant/Admin)
- **Body**:
```json
{
  "status": "pending|accepted|in_transit|delivered|cancelled"
}
```
- **Status Workflow**:
  - `pending` → `accepted` (by Merchant/Admin)
  - `accepted` → `in_transit` (by Driver)
  - `in_transit` → `delivered` (by Driver)

#### 5. Assign Driver (Admin Only)
- **URL**: `/orders/api/{id}/assign/`
- **Method**: `PATCH`
- **Auth Required**: Yes (Admin role)
- **Body**:
```json
{
  "driver_id": 3
}
```

---

## Role-Based Access Control

### Customer
- Browse restaurants and menus
- Place orders
- View own orders
- Update profile

### Merchant
- Manage restaurants (CRUD)
- Manage menu items (CRUD)
- View orders for their restaurants
- Update order status to 'accepted'

### Driver
- View assigned deliveries
- Update order status (`accepted` → `in_transit` → `delivered`)
- View delivery details

### Admin
- Full access to all resources
- Assign drivers to orders
- Manage users, restaurants, and orders
- View platform statistics

---

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Error Response Format

```json
{
  "error": "Error message here",
  "detail": "Detailed error information"
}
```

---

## Example API Usage

### Using cURL

#### Login
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "customer1",
    "password": "password123"
  }'
```

#### Create Order
```bash
curl -X POST http://localhost:8000/orders/api/create/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "restaurant_id": 1,
    "delivery_address": "123 Main St",
    "notes": "Please ring doorbell",
    "items": [
      {"menu_item_id": "1", "quantity": "2"},
      {"menu_item_id": "2", "quantity": "1"}
    ]
  }'
```

### Using JavaScript Fetch

```javascript
// Login
const response = await fetch('http://localhost:8000/api/token/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'customer1',
    password: 'password123'
  })
});
const { access, refresh } = await response.json();

// Create Order
const orderResponse = await fetch('http://localhost:8000/orders/api/create/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${access}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    restaurant_id: 1,
    delivery_address: '123 Main St',
    items: [
      { menu_item_id: '1', quantity: '2' }
    ]
  })
});
```

---

## Testing Credentials

After running `python manage.py seed_data`:

- **Admin**: username=`admin`, password=`admin123`
- **Customer**: username=`customer1`, password=`password123`
- **Merchant**: username=`merchant1`, password=`password123`
- **Driver**: username=`driver1`, password=`password123`

---

## Web Interface URLs

- **Login**: http://localhost:8000/login/
- **Register**: http://localhost:8000/register/
- **Customer Dashboard**: http://localhost:8000/dashboard/customer/
- **Merchant Dashboard**: http://localhost:8000/dashboard/merchant/
- **Driver Dashboard**: http://localhost:8000/dashboard/driver/
- **Admin Dashboard**: http://localhost:8000/dashboard/admin/
- **Django Admin**: http://localhost:8000/admin/
