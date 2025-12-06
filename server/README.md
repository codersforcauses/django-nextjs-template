# Backend server

A template Django server showcasing idiomatic Django REST Framework patterns.

## Features

- **Django REST Framework**: Full-featured API with viewsets and routers
- **Filtering & Search**: Advanced filtering using django-filter
- **Pagination**: Configurable pagination for large datasets
- **Permissions**: Custom permission classes for fine-grained access control
- **Validation**: Field and object-level validation
- **Testing**: Comprehensive test suite with APITestCase

## Quick Start

### 1. Install Dependencies

```sh
# If not in dev container
uv sync

# Install django-filter
uv add django-filter
```

### 2. Run Migrations

```sh
uv run manage.py migrate
```

### 3. Create a Superuser (Optional)

```sh
uv run manage.py createsuperuser
```

### 4. Create Sample Data (Optional)

```sh
uv run manage.py create_sample_data
```

This creates:

- 5 habitats (Savanna, Rainforest, Arctic, Aquatic, Reptile House)
- 12 enclosures (Lions, Elephants, Penguins, Dolphins, etc.)
- 8 feeding schedules throughout the day

### 5. Run the Server

```sh
uv run manage.py runserver
```

The API will be available at:

- API Root: `http://localhost:8000/api/`
- Admin Interface: `http://localhost:8000/admin/`
- Browsable API: Navigate to any endpoint in your browser for an interactive interface

## API Endpoints

### Authentication

The API uses **JWT (JSON Web Token) authentication** with access and refresh tokens.

**Endpoints:**

- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login and receive JWT tokens
- `POST /api/auth/refresh/` - Refresh access token
- `POST /api/auth/logout/` - Logout (client-side token deletion)

#### Example - Register

```sh
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "keeper1", "email": "keeper1@zoo.com", "password": "password123"}'
```

**Response:**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "keeper1",
    "email": "keeper1@zoo.com"
  }
}
```

#### Example - Login

```sh
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "keeper1", "password": "password123"}'
```

**Response:** Same as register (returns `refresh`, `access`, and `user`)

#### Using JWT Tokens

Include the **access token** in the Authorization header with `Bearer` prefix:

```sh
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  http://localhost:8000/api/feedings/
```

#### Refreshing Tokens

Access tokens expire after 60 minutes. Use the refresh token to get a new access token:

```sh
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN_HERE"}'
```

**Response:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Browsable API Authentication

The API supports **two authentication methods**:

1. **JWT Authentication** (for API clients):

   - Include `Authorization: Bearer <access_token>` header in requests
   - Access tokens expire after 60 minutes
   - Refresh tokens expire after 7 days
   - Perfect for frontend apps, mobile apps, and scripts

2. **Session Authentication** (for browsable API):
   - Click "Log in" in the top-right corner when viewing any API endpoint in your browser
   - Login at `/api-auth/login/` with username and password
   - Your session is stored as a cookie automatically
   - Perfect for testing and exploring the API interactively

#### Test Credentials

Create sample users with:

```sh
uv run manage.py create_sample_users
```

Then login with:

- Username: `keeper1`, `keeper2`, or `keeper3`
- Password: `password123`

### Habitats

- `GET /api/habitats/` - List all habitats
- `GET /api/habitats/{id}/` - Retrieve a specific habitat

### Enclosures

- `GET /api/enclosures/` - List all active enclosures (supports filtering, search, ordering)
- `GET /api/enclosures/{id}/` - Retrieve a specific enclosure
- `POST /api/enclosures/` - Create an enclosure (admin only)
- `PUT /api/enclosures/{id}/` - Update an enclosure (admin only)
- `DELETE /api/enclosures/{id}/` - Delete an enclosure (admin only)

#### Filtering & Search Examples

```sh
# Filter by capacity range (number of animals)
GET /api/enclosures/?min_capacity=6&max_capacity=10

# Filter by habitat
GET /api/enclosures/?habitat=1

# Search by name
GET /api/enclosures/?search=lion

# Order by capacity (descending)
GET /api/enclosures/?ordering=-capacity

# Combine filters
GET /api/enclosures/?min_capacity=6&search=lion&ordering=name
```

### Feedings

- `GET /api/feedings/` - List all feedings (authenticated users only)
- `GET /api/feedings/{id}/` - Retrieve a specific feeding
- `POST /api/feedings/` - Create a feeding schedule (authenticated users only)
- `PUT /api/feedings/{id}/` - Update a feeding (keeper only)
- `DELETE /api/feedings/{id}/` - Delete a feeding (keeper only)

#### Filtering Examples

```sh
# Filter by room
GET /api/bookings/?room=1

# Filter by date
GET /api/bookings/?start_date=2025-01-15

# Filter by date range
GET /api/bookings/?start_after=2025-01-15T10:00:00Z&start_before=2025-01-16T18:00:00Z

# Order by start time (descending - most recent first)
GET /api/bookings/?ordering=-start_time
```

## Testing

### Run All Tests

```sh
uv run manage.py test
```

### Run Tests for Specific App

```sh
# Test zoo app
uv run manage.py test zoo

# Test bookings app
uv run manage.py test bookings
```

### Run Tests with Coverage

```sh
# Install coverage
uv add coverage

# Run tests with coverage
coverage run --source='.' manage.py test

# View coverage report
coverage report

# Generate HTML coverage report
coverage html
# Open htmlcov/index.html in browser
```

## Project Structure

```
server/
├── manage.py              # Django management script
├── pyproject.toml         # Python dependencies
├── server/               # Main project settings
│   ├── settings.py       # Django settings
│   └── urls.py          # URL routing
├── zoo/                 # Zoo app (habitats & enclosures)
│   ├── models.py        # Habitat and Enclosure models
│   ├── serializers.py   # DRF serializers
│   ├── views.py         # ViewSets
│   ├── urls.py          # Router configuration
│   ├── filters.py       # Custom filter classes
│   ├── permissions.py   # Custom permissions
│   └── tests.py         # Test suite
├── bookings/            # Feedings app
│   ├── models.py        # Feeding model
│   ├── serializers.py   # DRF serializers with validation
│   ├── views.py         # ViewSets
│   ├── urls.py          # Router configuration
│   ├── filters.py       # Custom filter classes
│   ├── permissions.py   # Custom permissions
│   └── tests.py         # Test suite
└── idiomatic-django.md  # Tutorial and best practices
```

## Admin Interface

Access the Django admin at `http://localhost:8000/admin/`

The admin interface allows you to:

- Manage habitats, enclosures, and feeding schedules
- View and edit all zoo data
- Create test data for development

## Development Tips

1. **Read the tutorial**: See `idiomatic-django.md` for detailed explanations
2. **Use the admin**: Great for quickly creating test data
3. **Check the tests**: Tests serve as documentation for expected behavior
4. **Try the filters**: Experiment with different query parameters
5. **Use DRF's browsable API**: Navigate to endpoints in your browser

## Common Commands

```sh
# Make migrations after model changes
uv run manage.py makemigrations

# Apply migrations
uv run manage.py migrate

# Run the development server
uv run manage.py runserver

# Run tests
uv run manage.py test

# Run linting
cd server && flake8

# Create a new app
uv run manage.py startapp appname
```
