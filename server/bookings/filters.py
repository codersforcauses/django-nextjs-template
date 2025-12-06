import django_filters
from .models import Feeding


class FeedingFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='start_time',
        lookup_expr='date'
    )
    start_after = django_filters.DateTimeFilter(
        field_name='start_time',
        lookup_expr='gte'
    )
    start_before = django_filters.DateTimeFilter(
        field_name='start_time',
        lookup_expr='lte'
    )
    enclosure = django_filters.NumberFilter(field_name='enclosure__id')
    
    class Meta:
        model = Feeding
        fields = ['enclosure', 'keeper']
