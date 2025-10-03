# Food Delivery Web Application

A Glovo-style food delivery platform built with Django, Django REST Framework, Tailwind CSS, and Vanilla JavaScript.

## Features

### User Roles
- **Customer**: Browse restaurants, place orders, track deliveries
- **Merchant**: Manage restaurants and menu items, view incoming orders
- **Driver**: View assigned deliveries, update delivery status
- **Admin**: Full platform management and monitoring

### Key Functionality
- JWT-based authentication with role-based access control
- Restaurant and menu management
- Order placement and tracking
- Real-time order status updates
- Driver assignment system
- Responsive design with Tailwind CSS
- RESTful API for all operations

## Tech Stack

- **Backend**: Django 4.2.7, Django REST Framework 3.14.0
- **Authentication**: JWT (Simple JWT)
- **Frontend**: Tailwind CSS (CDN), Vanilla JavaScript
- **Database**: SQLite (development)
- **Image Handling**: Pillow

## Project Structure

```
fooddelivery/
├── users/              # User authentication and role management
├── restaurants/        # Restaurant and menu item models/views
├── orders/             # Order processing and management
├── delivery/           # Driver profiles and delivery logic
├── dashboard/          # Role-based dashboard views
├── templates/          # HTML templates
├── static/             # CSS and JavaScript files
└── media/              # User-uploaded images
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Seed Database with Sample Data

```bash
python manage.py seed_data
```

This will create:
- 1 Admin user
- 3 Customers
- 3 Merchants with restaurants
- 3 Drivers
- Sample menu items for each restaurant
- 1 sample order

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit http://localhost:8000

## Default Login Credentials

After seeding:

| Role     | Username   | Password     |
|----------|------------|--------------|
| Admin    | admin      | admin123     |
| Customer | customer1  | password123  |
| Merchant | merchant1  | password123  |
| Driver   | driver1    | password123  |

## Color Theme

The application uses a **leafy green** and **carrot orange** color scheme:
- Primary (Leafy Green): `#4CAF50`
- Secondary (Carrot Orange): `#FF9800`

## API Documentation

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete REST API documentation.

## Web Interface

### Customer Features
- Browse restaurants with ratings and descriptions
- View detailed menus with categories
- Add items to cart
- Place orders with delivery address
- Track order status in real-time

### Merchant Features
- View all owned restaurants
- Monitor incoming orders
- View order details and customer information
- Manage menu availability

### Driver Features
- View assigned deliveries
- Update order status (Accepted → In Transit → Delivered)
- View customer and delivery information

### Admin Features
- Platform-wide statistics dashboard
- User management
- Restaurant management
- Order monitoring
- Driver assignment for pending orders
- Access to Django admin panel

## API Endpoints

### Authentication
- `POST /api/register/` - Register new user
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh token
- `GET /api/me/` - Get current user
- `GET/PUT/PATCH /api/profile/` - Manage profile

### Restaurants
- `GET /restaurants/api/` - List restaurants
- `POST /restaurants/api/` - Create restaurant (Merchant)
- `GET /restaurants/api/{id}/` - Get restaurant details
- `PUT/PATCH /restaurants/api/{id}/` - Update restaurant
- `DELETE /restaurants/api/{id}/` - Delete restaurant

### Menu Items
- `GET /restaurants/api/{restaurant_id}/menu/` - List menu items
- `POST /restaurants/api/{restaurant_id}/menu/` - Create menu item
- `GET /restaurants/api/menu/{id}/` - Get menu item
- `PUT/PATCH /restaurants/api/menu/{id}/` - Update menu item
- `DELETE /restaurants/api/menu/{id}/` - Delete menu item

### Orders
- `GET /orders/api/` - List orders (filtered by role)
- `POST /orders/api/create/` - Create order (Customer)
- `GET /orders/api/{id}/` - Get order details
- `PATCH /orders/api/{id}/status/` - Update order status
- `PATCH /orders/api/{id}/assign/` - Assign driver (Admin)

## Order Workflow

1. **Customer** places an order (status: `pending`)
2. **Admin** assigns a driver to the order
3. **Driver** accepts and starts delivery (status: `accepted` → `in_transit`)
4. **Driver** marks order as delivered (status: `delivered`)

## Role-Based Access Control

The application enforces strict role separation:
- Customers cannot access merchant/driver/admin features
- Merchants can only manage their own restaurants
- Drivers can only update orders assigned to them
- Admin has full access to all features

## Development Notes

### Adding New Restaurants/Menu Items

Use Django Admin panel:
1. Login as admin at http://localhost:8000/admin/
2. Navigate to Restaurants → Add Restaurant
3. Add menu items for the restaurant

Or use the REST API with merchant credentials.

### Creating New Orders via API

```bash
curl -X POST http://localhost:8000/orders/api/create/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "restaurant_id": 1,
    "delivery_address": "123 Main St",
    "items": [
      {"menu_item_id": "1", "quantity": "2"}
    ]
  }'
```

## JavaScript Features

### Real-time Order Updates
- Customer dashboard auto-refreshes order status every 10 seconds
- Driver dashboard auto-refreshes every 30 seconds for new assignments

### Shopping Cart
- Add items to cart
- Update quantities
- Remove items
- Cart persists during session

### AJAX API Calls
- All dynamic features use Fetch API
- CSRF token handling for secure POST/PATCH requests

## Database Models

### User
- Custom user model with role field
- Roles: customer, merchant, driver, admin
- Phone number and address fields

### Restaurant
- Belongs to a merchant
- Name, description, address, rating
- Active/inactive status

### MenuItem
- Belongs to a restaurant
- Name, description, price, category
- Image upload support
- Available/unavailable status

### Order
- Customer, restaurant, driver (optional)
- Status workflow: pending → accepted → in_transit → delivered
- Delivery address and notes
- Total amount

### OrderItem
- Menu item reference
- Quantity and price snapshot
- Auto-calculated subtotal

### DriverProfile
- One-to-one with driver user
- Vehicle information
- Availability status
- Rating and delivery count

## Future Enhancements

- Payment gateway integration
- Real-time notifications (WebSockets)
- Geolocation for driver tracking
- Customer reviews and ratings
- Restaurant search and filtering
- Email verification
- Password reset functionality
- Analytics dashboard

## License

MIT License - Feel free to use this project for learning or commercial purposes.

## Support

For issues or questions, please open an issue on the GitHub repository.
