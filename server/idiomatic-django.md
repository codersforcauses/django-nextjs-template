# Idiomatic Django

**Idiomatic code** follows the conventions and best practices of a language or framework.

Idiomatic Django is:

- **Declarative** - Define what you want, not how to do it
- **Convention over configuration** - Minimal boilerplate
- **Composition over inheritance** - Prefer to combine built-in mixins instead of overriding methods

This guide shows you how to build REST APIs using Django Rest Framework's powerful abstractions.

We'll build a Zoo Management System to demonstrate these concepts.

## Apps

Apps are modular components that organize your code. Plan them to avoid circular dependencies.

```sh
uv run manage.py startapp users     # eg. members, zookeeper ids
uv run manage.py startapp zoo       # eg. habitats, enclosures and animals
uv run manage.py startapp bookings  # eg. tickets, feedings
```

Add to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'users',
    'zoo',
    'bookings',
]
```

## Models

Define your models in `models.py` in each app.

```python
from django.db import models

class Habitat(models.Model):
    # id field is created automatically
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    # Common fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
```

## Admin

Register your models in `admin.py` to manage them via the Django Admin interface.

```python
from django.contrib import admin
from .models import Enclosure, Habitat

admin.site.register(Enclosure)
admin.site.register(Habitat)
```

## Migrations

After defining or modifying models, create and apply migrations.

```sh
python manage.py makemigrations
python manage.py migrate
```

You should avoid editing or deleting migration files unless you really know what you're doing, especially those that have already been merged into the main branch (deleting/editing migrations that others have already consumed is a **breaking change**).

Instead, make new migrations every time you modify the database schema (although you might want to squash any migrations that you have developed locally before merging to main).

---

This is a good point to commit your changes and raise a pull request!

---

## Serializers, Viewsets, Routers

### Serializers

These three go hand-in-hand to create RESTful APIs quickly and idiomatically.

Serializers define how model instances are converted to/from JSON. If we wanted Enclosure objects to take this format:

```json
{
  "id": 1,
  "name": "Lion Enclosure",
  "capacity": 6,
  "is_active": true,
  "habitat": {
    "id": 1,
    "name": "African Savanna",
    "location": "North Wing"
  }
}
```

We would define a serializer like so:

```python
# zoo/serializers.py
from rest_framework import serializers
from .models import Enclosure, Habitat


class HabitatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitat
        fields = ['id', 'name', 'location'] # prefer explicit fields over '__all__'

class EnclosureDetailSerializer(serializers.ModelSerializer):
    habitat = HabitatSerializer(read_only=True)

    class Meta:
        model = Enclosure
        fields = [
            'id', 'name', 'capacity', 'is_active', 'habitat'
        ]
```

### Viewsets

Viewsets combine the logic for a set of related views in a single class. They automatically provide implementations for common actions like list, retrieve, create, update, and delete.

In this case, we only want a read-only viewset for Enclosures, because we don't want users to modify them via the API. Staff users can manage them via the Admin interface instead.

```python
# zoo/views.py
from rest_framework import viewsets
from .models import Enclosure
from .serializers import EnclosureSerializer

class EnclosureViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Whatever you write here will show up in the API docs! 🦘
    """
    queryset = Enclosure.objects.all()
    serializer_class = EnclosureSerializer
    # ...
```

The `ReadOnlyModelViewSet` is a combination of these classes:

- `mixins.ListModelMixin` providing a `list()` method for GET /enclosures/
- `mixins.RetrieveModelMixin` providing a `retrieve()` method for GET /enclosures/{id}/
- `viewsets.GenericViewSet` providing the base functionality

A great resource for reviewing class methods is https://www.cdrf.co/.

DRF ViewSets are preferred over basic APIViews because you get a browsable API via the DRF web interface, which adds **discoverability** to your API surface.

### Routers

```python
# zoo/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import EnclosureViewSet

router = DefaultRouter() # will be imported by server/urls.py

router.register(r'enclosures',  # plural
                EnclosureViewSet,
                basename='enclosure') # singular
```

And finally, import each app's routers in the main `server/urls.py`:

```python
from django.contrib import admin
from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter
from rest_framework.routers import APIRootView

from zoo.urls import router as enclosures_router
from bookings.urls import router as feedings_router

router = DefaultRouter()
router.APIRootView = APIRootView
router.registry.extend(enclosures_router.registry)
router.registry.extend(feedings_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/healthcheck/", include("healthcheck.urls")),
    path('api/', include(router.urls)),
]
```

Try to keep your URL structure **flat** and avoid deep nesting where possible. Use query parameters for filtering instead.

---

Another good point to raise a pull request!

Note: still no tests yet. Question for the audience, why not?

---

## Authentication

Django Rest Framework provides multiple authentication schemes. For modern APIs, JWT (JSON Web Token) authentication is preferred for its stateless, scalable design.

### Setup JWT Authentication

Install and configure `djangorestframework-simplejwt`:

```sh
uv add djangorestframework-simplejwt
```

```python
# settings.py
from datetime import timedelta

INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework_simplejwt',  # Add this
    # ...
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
```

### Authentication ViewSet

Create authentication endpoints using a ViewSet

See the implemntation in `users/views.py`.

### Using JWT Tokens

Include the access token in API requests with the `Bearer` prefix:

```sh
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
     http://localhost:8000/api/feedings/
```

Access tokens expire after 60 minutes. Use the refresh token to get a new one:

```sh
curl -X POST http://localhost:8000/api/auth/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

### Permission Classes

Control access with built-in permission classes:

```python
from rest_framework import permissions

class FeedingViewSet(viewsets.ModelViewSet):
    queryset = Feeding.objects.all()
    serializer_class = FeedingSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require authentication
```

**Built-in Permission Classes**:

- `AllowAny` - No authentication required (default)
- `IsAuthenticated` - Must be logged in
- `IsAuthenticatedOrReadOnly` - Read-only for anonymous, full access for authenticated
- `IsAdminUser` - Must be staff user (admin)

### Custom Permissions

Create custom permission classes for fine-grained control:

```python
# bookings/permissions.py
from rest_framework import permissions

class IsKeeperOrReadOnly(permissions.BasePermission):
    """
    Only the keeper who created the feeding can edit/delete it.
    Others can only read.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for the keeper
        return obj.keeper == request.user.username


# In views.py
from .permissions import IsKeeperOrReadOnly

class FeedingViewSet(viewsets.ModelViewSet):
    queryset = Feeding.objects.all()
    serializer_class = FeedingSerializer
    permission_classes = [permissions.IsAuthenticated, IsKeeperOrReadOnly]
```

This prevents users from creating feedings for other keepers.

---

## Advanced Serializers

This allows you to:

- **Read**: Get full habitat details when retrieving an enclosure
- **Write**: Only need to provide `habitat_id` when creating/updating an enclosure

### Custom Validation

Add field-level or object-level validation:

```python
class FeedingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeding
        fields = '__all__'

    def validate_end_time(self, value):
        """Field-level validation"""
        if value < timezone.now():
            raise serializers.ValidationError("End time cannot be in the past")
        return value

    def validate(self, data):
        """Object-level validation"""
        if data['end_time'] <= data['start_time']:
            raise serializers.ValidationError(
                "End time must be after start time"
            )

        # Check for overlapping feedings
        overlapping = Feeding.objects.filter(
            enclosure=data['enclosure'],
            start_time__lt=data['end_time'],
            end_time__gt=data['start_time']
        )
        if self.instance:
            overlapping = overlapping.exclude(pk=self.instance.pk)

        if overlapping.exists():
            raise serializers.ValidationError(
                "This enclosure already has a feeding scheduled for this time"
            )

        return data
```

---

## Pagination

Pagination splits large result sets into pages, improving performance and user experience.

### Setup

In `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

### PageNumberPagination

Standard page-based pagination:

```python
# Custom pagination class
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'  # Allow client to set page size
    max_page_size = 100


class EnclosureViewSet(viewsets.ModelViewSet):
    queryset = Enclosure.objects.all()
    serializer_class = EnclosureSerializer
    pagination_class = StandardResultsSetPagination
```

---

## Filtering and Sorting

### Setup

Install django-filter:

```sh
uv add django-filter
```

Add to `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'django_filters',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

### Simple Filtering

```python
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class EnclosureViewSet(viewsets.ModelViewSet):
    queryset = Enclosure.objects.all()
    serializer_class = EnclosureSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['capacity', 'is_active', 'habitat']
    search_fields = ['name', 'habitat__name']
    ordering_fields = ['name', 'capacity', 'id']
    ordering = ['name']  # Default ordering

# Usage:
# /api/enclosures/?capacity=10
# /api/enclosures/?is_active=true
# /api/enclosures/?habitat=1
# /api/enclosures/?search=lion
# /api/enclosures/?ordering=-capacity  # Descending
```

## Testing

Testing ensures your API works correctly and continues to work as you make changes.

### Basic Test Structure

```python
# zoo/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Habitat, Enclosure


class EnclosureAPITestCase(APITestCase):
    def setUp(self):
        """Set up test data before each test"""
        self.habitat = Habitat.objects.create(
            name="African Savanna",
            location="North Wing"
        )
        self.enclosure = Enclosure.objects.create(
            name="Lion Enclosure",
            capacity=6,
            is_active=True,
            habitat=self.habitat
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_list_enclosures(self):
        """Test retrieving list of enclosures"""
        url = '/api/enclosures/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]['name'],
            'Lion Enclosure'
        )

    def test_retrieve_enclosure(self):
        """Test retrieving a single enclosure"""
        url = f'/api/enclosures/{self.enclosure.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Lion Enclosure')
        self.assertEqual(response.data['capacity'], 6)

    def test_create_enclosure_unauthenticated(self):
        """Test that unauthenticated users cannot create enclosures"""
        url = '/api/enclosures/'
        data = {
            'name': 'New Enclosure',
            'capacity': 4,
            'is_active': True,
            'habitat_id': self.habitat.id
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_enclosure_authenticated(self):
        """Test creating an enclosure when authenticated"""
        self.client.force_authenticate(user=self.user)
        url = '/api/enclosures/'
        data = {
            'name': 'New Enclosure',
            'capacity': 4,
            'is_active': True,
            'habitat_id': self.habitat.id
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enclosure.objects.count(), 2)
        self.assertEqual(response.data['name'], 'New Enclosure')

    def test_update_enclosure(self):
        """Test updating an enclosure"""
        self.client.force_authenticate(user=self.user)
        url = f'/api/enclosures/{self.enclosure.id}/'
        data = {
            'name': 'Updated Enclosure Name',
            'capacity': 8,
            'is_active': True,
            'habitat_id': self.habitat.id
        }
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.enclosure.refresh_from_db()
        self.assertEqual(self.enclosure.name, 'Updated Enclosure Name')
        self.assertEqual(self.enclosure.capacity, 8)

    def test_delete_enclosure(self):
        """Test deleting an enclosure"""
        self.client.force_authenticate(user=self.user)
        url = f'/api/enclosures/{self.enclosure.id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Enclosure.objects.count(), 0)

    def test_filter_by_capacity(self):
        """Test filtering enclosures by capacity"""
        Enclosure.objects.create(
            name="Elephant Enclosure",
            capacity=10,
            is_active=True,
            habitat=self.habitat
        )
        url = '/api/enclosures/?min_capacity=8'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Elephant Enclosure')

    def test_search_enclosures(self):
        """Test searching enclosures by name"""
        url = '/api/enclosures/?search=Lion'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
```

---

## Useful tools

- [Classy Django REST Framework](https://www.cdrf.co/)
- [Classy Class-Based Views](https://ccbv.co.uk/)
