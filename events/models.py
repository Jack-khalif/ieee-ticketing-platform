import uuid
from django.db import models
from django.utils import timezone

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    CATEGORY_CHOICES = [
        ('hackathon', 'Hackathons'),
        ('tech-summit', 'Tech Summits'),
        ('workshop', 'Workshops'),
        ('networking', 'Networking'),
        ('campus', 'Campus Life'),
        ('club', 'Clubs'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    capacity = models.IntegerField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='posters/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='campus')

    @property
    def is_past(self):
        return self.date < timezone.now()

    def __str__(self):
        return self.title