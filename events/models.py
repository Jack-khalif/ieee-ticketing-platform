from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField()
    organizer = models.CharField(max_length=200)

    def __str__(self):
        return self.title