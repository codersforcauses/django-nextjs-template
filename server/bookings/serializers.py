from rest_framework import serializers
from django.utils import timezone
from .models import Feeding


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
                "This enclosure is already scheduled for feeding "
                "during this time"
            )

        return data
