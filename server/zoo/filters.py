import django_filters
from .models import Enclosure


class EnclosureFilter(django_filters.FilterSet):
    min_capacity = django_filters.NumberFilter(
        field_name='capacity',
        lookup_expr='gte'
    )
    max_capacity = django_filters.NumberFilter(
        field_name='capacity',
        lookup_expr='lte'
    )
    name = django_filters.CharFilter(lookup_expr='icontains')
    habitat_name = django_filters.CharFilter(
        field_name='habitat__name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Enclosure
        fields = ['is_active', 'habitat']
