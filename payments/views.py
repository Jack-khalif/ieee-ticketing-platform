from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Payment
from tickets.models import Ticket
from django.contrib.auth.models import User


class InitiatePaymentAPIView(APIView):

    def post(self, request):

        ticket_id = request.data.get("ticket_id")
        user_id = request.data.get("user_id")

        try:
            ticket = Ticket.objects.get(id=ticket_id)
            user = User.objects.get(id=user_id)

        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=404)

        payment = Payment.objects.create(
            user=user,
            ticket=ticket,
            amount=ticket.price
        )

        return Response({
            "message": "STK Push sent (simulated)",
            "payment_id": payment.id
        })
    

'''
SIMULATION OF MOBILE MONEY
'''
class ConfirmPaymentAPIView(APIView):

    def post(self, request):

        payment_id = request.data.get("payment_id")

        try:
            payment = Payment.objects.get(id=payment_id)

        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        payment.status = "completed"
        payment.transaction_id = "MPESA123456"
        payment.save()

        ticket = payment.ticket

        ticket.status = "sold"
        ticket.buyer = payment.user
        ticket.generate_qr_code()
        ticket.save()

        return Response({
            "message": "Payment confirmed. Ticket activated."
        })