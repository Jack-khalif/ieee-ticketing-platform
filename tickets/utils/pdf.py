from reportlab.pdfgen import canvas
from django.conf import settings
import os

def generate_ticket_pdf(ticket):

    filename = f"ticket_{ticket.id}.pdf"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    c = canvas.Canvas(filepath)

    c.drawString(100, 750, "EVENT TICKET")
    c.drawString(100, 720, f"Event: {ticket.event.name}")
    c.drawString(100, 700, f"Buyer: {ticket.buyer.username}")
    c.drawString(100, 680, f"Ticket ID: {ticket.id}")

    if ticket.qr_code:
        c.drawImage(ticket.qr_code.path, 100, 550, width=150, height=150)

    c.save()

    return filepath