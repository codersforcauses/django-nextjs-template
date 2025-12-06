from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Feeding
from .serializers import FeedingSerializer
from .filters import FeedingFilter
from .permissions import IsOwnerOrReadOnly


class FeedingViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides CRUD operations for feedings.
    
    Features:
    - Filtering by date, enclosure, and keeper
    - Search capabilities
    - Ordering by start time
    - Owner-based permissions
    """
    queryset = Feeding.objects.all()
    serializer_class = FeedingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = FeedingFilter
    search_fields = ['keeper', 'enclosure__name']
    ordering_fields = ['start_time', 'end_time']
    ordering = ['-start_time']
    
    def perform_create(self, serializer):
        """Automatically set the keeper to the current user"""
        serializer.save(keeper=self.request.user.username)
