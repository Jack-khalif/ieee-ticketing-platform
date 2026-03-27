from rest_framework import serializers
from .models import Event # Ensure this matches your actual model name!

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__' # This tells Django to accept all fields (title, date, image, etc.)