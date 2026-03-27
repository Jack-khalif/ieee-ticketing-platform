from rest_framework import status, generics
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

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
    # --- X-RAY DEBUGGING ---
    print("\n=== INCOMING UPLOAD DATA ===")
    print("TEXT DATA:", request.data)
    print("FILE DATA:", request.FILES) 
    print("============================\n")
    # -----------------------

    serializer = EventSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    print("VALIDATION ERRORS:", serializer.errors) 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)