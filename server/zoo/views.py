from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Enclosure, Habitat
from .serializers import EnclosureSerializer, HabitatSerializer
from .filters import EnclosureFilter
from .permissions import IsAdminOrReadOnly


class HabitatViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset that provides list and retrieve actions for habitats.
    """
    queryset = Habitat.objects.all()
    serializer_class = HabitatSerializer
    permission_classes = [permissions.AllowAny]


class EnclosureViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides CRUD operations for enclosures.

    Features:
    - Filtering by capacity, active status, and habitat
    - Search by name and habitat name
    - Ordering by name, capacity, or id
    - Admin-only write permissions
    """
    queryset = Enclosure.objects.all()
    serializer_class = EnclosureSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = EnclosureFilter
    search_fields = ['name', 'habitat__name']
    ordering_fields = ['name', 'capacity', 'id']
    ordering = ['name']

    def get_queryset(self):
        """Override to filter only active enclosures on list"""
        queryset = super().get_queryset()
        if self.action == 'list':
            queryset = queryset.filter(is_active=True)
        return queryset
