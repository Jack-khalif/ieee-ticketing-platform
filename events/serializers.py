from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    is_past = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = '__all__'