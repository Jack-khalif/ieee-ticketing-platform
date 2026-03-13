from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import qrcode


def generate_ticket_pdf(ticket):
    buffer = BytesIO()

    c = canvas.Canvas(buffer)

    # Ticket text
    c.drawString(100, 750, "Event Ticket")
    c.drawString(100, 720, f"Event: {ticket.event.title}")
    c.drawString(100, 700, f"Ticket ID: {ticket.id}")
    c.drawString(100, 680, f"Buyer: {ticket.buyer.username}")

    # -------- Generate QR Code --------
    qr_data = f"TICKET-{ticket.id}"

    qr = qrcode.make(qr_data)

    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)

    qr_image = ImageReader(qr_buffer)

    # place QR on the PDF
    c.drawImage(qr_image, 400, 650, width=150, height=150)

    c.save()

    pdf = buffer.getvalue()
    buffer.close()

    # Save locally for testing
    with open(f"ticket_{ticket.id}.pdf", "wb") as f:
        f.write(pdf)

    return pdf