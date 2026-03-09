from django.db import models

# Create your models here.
from events.models import Event
from django.contrib.auth.models import User

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('checked_in', 'Checked In'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.event.title} - {self.status}"