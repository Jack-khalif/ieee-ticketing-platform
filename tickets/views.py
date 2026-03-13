from rest_framework import generics, status
from rest_framework.response import Response
from .models import Ticket
from .serializers import TicketSerializer
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import render

class TicketPurchaseAPIView(generics.GenericAPIView):
    serializer_class = TicketSerializer

    def post(self, request, *args, **kwargs):
        ticket_id = request.data.get('ticket_id')
        user_id = request.data.get('user_id')

        try:
            ticket = Ticket.objects.get(id=ticket_id)
            user = User.objects.get(id=user_id)
        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if ticket.status != 'available':
            return Response({'error': 'Ticket already sold or checked in'}, status=status.HTTP_400_BAD_REQUEST)

        ticket.buyer = user
        ticket.status = 'sold'
        ticket.purchase_date = timezone.now()

        ticket.generate_qr_code()
    
        ticket.save()

        serializer = self.get_serializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)
    '''
    This API view allows users to purchase tickets.  
    - It expects a POST request with ticket_id and user_id in the request data.
    - It checks if the ticket exists and is available, and if the user exists.
    - If everything is valid, it updates the ticket’s buyer and status to “sold”, and returns the updated ticket data in the response.
        
    '''
class ScanTicketAPIView(APIView):

    def post(self, request):

        ticket_id = request.data.get("ticket_id")

        try:
            ticket = Ticket.objects.get(id=ticket_id)

        except Ticket.DoesNotExist:
            return Response(
                {"message": "Invalid ticket"},
                status=status.HTTP_404_NOT_FOUND
            )

        if ticket.status == "checked_in":
            return Response(
                {"message": "Ticket already used"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if ticket.status != "sold":
            return Response(
                {"message": "Ticket not purchased"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ticket.status = "checked_in"
        ticket.save()

        return Response(
            {"message": "Entry allowed"},
            status=status.HTTP_200_OK
        )
'''
this logic scans the ticket, finds ticket in database, checks the status
then updates to checked_in

'''
class ValidateTicketAPIView(APIView):

    def post(self, request):

        ticket_id = request.data.get("ticket_id")

        try:
            ticket = Ticket.objects.get(id=ticket_id)

        except Ticket.DoesNotExist:
            return Response({"valid": False})

        if ticket.status != "sold":
            return Response({"valid": False})

        if ticket.checked_in:
            return Response({
                "valid": False,
                "message": "Ticket already used"
            })

        ticket.checked_in = True
        ticket.save()

        return Response({
            "valid": True,
            "message": "Welcome to the event"
        })
    '''
    AT THE EVENT ENTRANCE, A SCANNER CHECKS TICKETS.
    '''
def verify_ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)

        if ticket.checked_in:
            return JsonResponse({
                "valid": False,
                "message": "Ticket already used"
            })

        return JsonResponse({
            "valid": True,
            "event": ticket.event.title,
            "buyer": ticket.buyer.username
        })

    except Ticket.DoesNotExist:
        return JsonResponse({
            "valid": False,
            "message": "Invalid ticket"
        })
def scanner_page(request):
    return render(request, "tickets/scanner.html")