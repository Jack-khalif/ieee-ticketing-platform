from django.db import models
from django.contrib.auth.models import User
from events.models import Event


class Ticket(models.Model):

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('checked_in', 'Checked In'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    purchase_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.event.title} Ticket #{self.id}"