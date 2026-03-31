from rest_framework import status, generics
from rest_framework.decorators import api_view, parser_classes , permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Event
from .serializers import EventSerializer

# ==========================================
# 1. THE RESTORED LIST VIEW
# (This serves data to your React Home Page)
# ==========================================
class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.all().order_by('-id') # Shows newest events first
    serializer_class = EventSerializer
class EventDetailAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
# ==========================================
# 2. THE NEW CREATE VIEW
# (This handles the FormData and Image Uploads)
# ==========================================
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser]) 
def create_event(request):
    serializer = EventSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    print(serializer.errors) # Helpful for terminal debugging
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_event(request, pk):
    """Allows the organizer to update event details (like changing the location or time)."""
    event = get_object_or_404(Event, pk=pk)
    
    # Security check: Only the owner can edit this!
    # (If your field is named 'user' instead of 'organizer', change it below)
    if event.organizer != request.user:
        return Response({"error": "You do not have permission to edit this event."}, status=status.HTTP_403_FORBIDDEN)
    
    data = request.data

    # Update fields only if they are provided in the request
    if 'title' in data:
        event.title = data['title']
    if 'ticket_price' in data:
        event.ticket_price = data['ticket_price']
    if 'date' in data:
        event.date = data['date'] # Expects standard ISO format (YYYY-MM-DDTHH:MM)
    
    # If they uploaded a new poster image
    if 'image' in request.FILES:
        event.image = request.FILES['image']

    try:
        event.save()
        return Response({
            "message": "Event updated successfully!",
            "event": {
                "id": event.id,
                "title": event.title,
                "ticket_price": event.ticket_price
            }
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)