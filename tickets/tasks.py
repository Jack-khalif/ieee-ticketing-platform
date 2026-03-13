from django.core.mail import EmailMessage
from tickets.utils.pdf import generate_ticket_pdf # your PDF generator

def send_ticket_email(ticket):
    pdf = generate_ticket_pdf(ticket)
    email = EmailMessage(
        subject=f"Your Ticket for {ticket.event.title}",
        body="Attached is your ticket.",
        to=[ticket.buyer.email],
    )
    email.attach(f"ticket_{ticket.id}.pdf", pdf, "application/pdf")
    email.send()