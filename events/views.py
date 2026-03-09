from rest_framework import generics
from .models import Event
from .serializers import EventSerializer

class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

'''
This is a simple API view that lists all events.
- generics.ListAPIView → a built-in view that provides a read-only endpoint to list all instances of a model.
- queryset → defines which data to retrieve (all events).
- serializer_class → specifies how to convert the Event objects into JSON format for the API response.
'''