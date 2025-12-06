from rest_framework import serializers
from django.utils import timezone
from .models import Enclosure, Habitat


class HabitatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitat
        fields = ['id', 'name', 'location']


class EnclosureSerializer(serializers.ModelSerializer):
    habitat = HabitatSerializer(read_only=True)
    habitat_id = serializers.PrimaryKeyRelatedField(
        queryset=Habitat.objects.all(),
        source='habitat',
        write_only=True
    )
    feeding_count = serializers.SerializerMethodField()
    is_available_now = serializers.SerializerMethodField()

    class Meta:
        model = Enclosure
        fields = [
            'id', 'name', 'capacity', 'is_active',
            'habitat', 'habitat_id',
            'feeding_count', 'is_available_now'
        ]

    def get_feeding_count(self, obj):
        """Return the number of feedings for this enclosure"""
        return obj.feeding_set.count()

    def get_is_available_now(self, obj):
        """Check if enclosure is available right now"""
        now = timezone.now()
        return not obj.feeding_set.filter(
            start_time__lte=now,
            end_time__gte=now
        ).exists()
