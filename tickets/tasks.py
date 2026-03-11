from celery import shared_task
from django.core.mail import EmailMessage
from .models import Ticket
from .utils.pdf import generate_ticket_pdf


@shared_task
def send_ticket_email(email, ticket_id):

    ticket = Ticket.objects.get(id=ticket_id)

    pdf_path = generate_ticket_pdf(ticket)

    mail = EmailMessage(
        subject="Your Event Ticket",
        body="Attached is your ticket.",
        to=[email]
    )

    mail.attach_file(pdf_path)

    mail.send()