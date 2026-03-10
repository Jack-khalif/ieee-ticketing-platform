from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event
from tickets.models import Ticket


@receiver(post_save, sender=Event)
def create_tickets(sender, instance, created, **kwargs):
    
    if created:
        tickets = [
            Ticket(
                event=instance,
                price=instance.ticket_price
            )
            for _ in range(instance.capacity)
        ]

        Ticket.objects.bulk_create(tickets)