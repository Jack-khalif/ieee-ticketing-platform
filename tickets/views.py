from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from events.models import Event
from .models import Ticket

@api_view(['POST'])
@permission_classes([AllowAny]) # 👈 We allow guests to hit this endpoint!
def purchase_tickets(request):
    data = request.data
    event_id = data.get('event_id')
    quantity = int(data.get('quantity', 1))
    is_guest = data.get('is_guest', False)
    
    # 1. Find the Event we are buying tickets for
    event = get_object_or_404(Event, id=event_id)
    
    created_tickets = []
    
    # 2. THE TICKET PRINTER: Loop through the quantity and mint them one by one
    for _ in range(quantity):
        if is_guest:
            # Mint a Guest Ticket
            ticket = Ticket.objects.create(
                event=event,
                guest_name=data.get('guest_name'),
                guest_email=data.get('guest_email')
            )
        else:
            # Mint a User Ticket (DRF handles figuring out who the user is from the Token!)
            ticket = Ticket.objects.create(
                event=event,
                user=request.user if request.user.is_authenticated else None
            )
        
        # Save the unique ID so we can send it back to React
        created_tickets.append(ticket.ticket_id)
        
    # 3. Send the receipt back to React
    return Response({
        "message": "Tickets minted successfully!",
        "event": event.title,
        "quantity": quantity,
        "ticket_ids": created_tickets # e.g., ["TIX-1A2B3C4D", "TIX-5E6F7G8H"]
    }, status=status.HTTP_201_CREATED)