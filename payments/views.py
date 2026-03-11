from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Payment
from tickets.models import Ticket
from django.contrib.auth.models import User

from tickets.tasks import send_ticket_email
from payments.daraja import stk_push


class InitiatePaymentAPIView(APIView):

    def post(self, request):

        ticket_id = request.data.get("ticket_id")
        user_id = request.data.get("user_id")
        phone = request.data.get("phone")

        try:
            ticket = Ticket.objects.get(id=ticket_id)
            user = User.objects.get(id=user_id)

        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=404)

        payment = Payment.objects.create(
            user=user,
            ticket=ticket,
            amount=ticket.price,
            status="pending"
        )

        stk_response = stk_push(
            phone,
            ticket.price,
            f"TICKET-{ticket.id}"
        )

        payment.merchant_request_id = stk_response.get("MerchantRequestID")
        payment.checkout_request_id = stk_response.get("CheckoutRequestID")

        payment.save()

        return Response({
            "message": "STK Push sent",
            "payment_id": payment.id,
            "mpesa_response": stk_response
        })


class MpesaCallbackAPIView(APIView):

    def post(self, request):

        data = request.data

        callback = data["Body"]["stkCallback"]

        checkout_request_id = callback["CheckoutRequestID"]
        result_code = callback["ResultCode"]

        try:
            payment = Payment.objects.get(
                checkout_request_id=checkout_request_id
            )
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"})

        if result_code == 0:

            payment.status = "completed"
            payment.transaction_id = "MPESA_SUCCESS"

            ticket = payment.ticket
            ticket.status = "sold"
            ticket.buyer = payment.user

            ticket.generate_qr_code()

            ticket.save()

            send_ticket_email.delay(payment.user.email, ticket.id)

        else:

            payment.status = "failed"

        payment.save()

        return Response({"message": "Callback received"})