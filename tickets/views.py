from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny , IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from events.models import Event
from .models import Ticket

@api_view(['POST'])
@permission_classes([AllowAny])
def purchase_tickets(request):
    data = request.data
    event_id = data.get('event_id')
    
    # 🚀 NEW: We now expect an array of attendees from React!
    # Example: [{"name": "Jane", "email": "jane@mail.com"}, {"name": "John", "email": "john@mail.com"}]
    attendees = data.get('attendees', []) 
    
    event = get_object_or_404(Event, id=event_id)
    created_tickets = []
    
    # 1. Who is the actual buyer? (This safely fixes the AnonymousUser bug!)
    actual_user = request.user if request.user.is_authenticated else None

    # 2. Mint a unique ticket for EVERY person in the attendees list
    for attendee in attendees:
        ticket = Ticket.objects.create(
            event=event,
            user=actual_user, # If logged in, this attaches all 3 tickets to the buyer's account!
            guest_name=attendee.get('name'),
            guest_email=attendee.get('email')
        )
        created_tickets.append(ticket.ticket_id)
        
    # 3. THE EMAIL ENGINE: Send one master receipt to the main buyer
    if attendees:
        buyer_email = attendees[0].get('email')
        buyer_name = attendees[0].get('name')
        
        ticket_list_string = "\n".join([f"- {tid}" for tid in created_tickets])
        
        subject = f"Your Tickets for {event.title}"
        message = f"""Hi {buyer_name},

You're going to {event.title}!

Here are your Ticket IDs. Have them ready to show at the door:
{ticket_list_string}

See you there!
The Events Team"""
        
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [buyer_email], fail_silently=False)
            print(f"✅ SUCCESS: Email sent to {buyer_email}")
        except Exception as e:
            print(f"❌ EMAIL ERROR: {e}")

    return Response({
        "message": "Tickets minted successfully!",
        "event": event.title,
        "quantity": len(created_tickets),
        "ticket_ids": created_tickets
    }, status=status.HTTP_201_CREATED)
@api_view(['POST'])
@permission_classes([AllowAny]) # Note: In a production app, we would restrict this to Organizers only!
def scan_ticket(request):
    ticket_id = request.data.get('ticket_id')

    if not ticket_id:
        return Response({"error": "No ticket ID provided."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 1. Look for the ticket in the database
        ticket = Ticket.objects.get(ticket_id=ticket_id)
        
        # Helper variable to get the buyer's name
        buyer_name = ticket.user.username if ticket.user else ticket.guest_name

        # 2. Did they already use this ticket?
        if ticket.is_scanned:
            return Response({
                "status": "error",
                "message": "ALREADY SCANNED",
                "details": f"Ticket belongs to {buyer_name} but was already used."
            }, status=status.HTTP_400_BAD_REQUEST)

        # 3. If it's valid, mark it as used so they can't pass it to a friend!
        ticket.is_scanned = True
        ticket.save()

        return Response({
            "status": "success",
            "message": "VALID TICKET",
            "details": f"Admit 1: {buyer_name} to {ticket.event.title}"
        }, status=status.HTTP_200_OK)

    except Ticket.DoesNotExist:
        # 4. They scanned a fake or deleted ticket
        return Response({
            "status": "error",
            "message": "INVALID TICKET",
            "details": "This ticket does not exist in the database."
        }, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
@permission_classes([AllowAny]) # Note: In production, we'd lock this to the Event Creator!
def event_dashboard(request, event_id):
    # 1. Grab the event
    event = get_object_or_404(Event, id=event_id)
    
    # 2. Get all tickets for this specific event, ordered by newest first
    tickets = Ticket.objects.filter(event=event).order_by('-purchase_date')

    # 3. Calculate the stats!
    total_sold = tickets.count()
    total_revenue = float(event.ticket_price) * total_sold
    scanned_count = tickets.filter(is_scanned=True).count()

    # 4. Create a clean list of the latest buyers for our React table
    sales_data = []
    for t in tickets[:10]: # Just grab the 10 most recent sales for the preview
        buyer_name = t.user.username if t.user else t.guest_name
        buyer_email = t.user.email if t.user else t.guest_email
        
        sales_data.append({
            "ticket_id": t.ticket_id,
            "buyer": buyer_name or "Unknown Guest",
            "email": buyer_email or "No email provided",
            "date": t.purchase_date.strftime("%b %d, %Y - %H:%M"),
            "is_scanned": t.is_scanned
        })

    # 5. Ship it to the frontend!
    return Response({
        "event_title": event.title,
        "total_sold": total_sold,
        "total_revenue": total_revenue,
        "scanned_count": scanned_count,
        "recent_sales": sales_data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_event_blast(request, event_id):
    """Allows an organizer to send an email to everyone who bought a ticket."""
    event = get_object_or_404(Event, id=event_id)
    
    # Security: Only the organizer can send blasts!
    # (If your field is named 'user' instead of 'organizer', change it below)
    if event.organizer != request.user: 
        return Response({"error": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)
        
    subject = request.data.get('subject')
    message = request.data.get('message')
    
    if not subject or not message:
        return Response({"error": "Subject and message are required."}, status=status.HTTP_400_BAD_REQUEST)

    # 1. Gather all unique emails from people who bought tickets
    tickets = Ticket.objects.filter(event=event)
    recipient_emails = set() # Using a 'set' automatically removes duplicates
    
    for t in tickets:
        email = t.user.email if t.user else t.guest_email
        if email:
            recipient_emails.add(email)
            
    if not recipient_emails:
        return Response({"message": "No attendees to email yet."}, status=status.HTTP_200_OK)

    # 2. Add a footer so they know why they are getting this
    full_message = f"{message}\n\n---\nThis message was sent by the organizer of {event.title}."

    # 3. Send the blast! (We use BCC so guests don't see each other's emails)
    from django.core.mail import EmailMessage
    email = EmailMessage(
        subject=f"[Update: {event.title}] {subject}",
        body=full_message,
        from_email='tickets@campustix.com',
        to=['tickets@campustix.com'], # Sent to ourselves
        bcc=list(recipient_emails)    # BCC'd to all attendees!
    )
    email.send(fail_silently=False)

    return Response({
        "message": f"Email blasted successfully to {len(recipient_emails)} attendees!"
    }, status=status.HTTP_200_OK)