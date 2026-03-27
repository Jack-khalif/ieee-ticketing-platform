import uuid
from django.db import models
from django.contrib.auth.models import User
from events.models import Event # We import the Event model so we can link to it!

class Ticket(models.Model):
    # 1. WHAT ARE THEY GOING TO?
    # related_name='tickets' allows us to easily find all tickets for a specific event
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    
    # 2. WHO BOUGHT IT? (Handles both Logged In users and Guests)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    guest_name = models.CharField(max_length=100, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)
    
    # 3. THE TICKET ITSELF
    ticket_id = models.CharField(max_length=20, unique=True, blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_scanned = models.BooleanField(default=False) # For the organizers at the door!

    def save(self, *args, **kwargs):
        # Automatically generate a unique 8-character ticket code if it doesn't exist
        if not self.ticket_id:
            # Example: "TIX-A1B2C3D4"
            self.ticket_id = f"TIX-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        owner = self.user.username if self.user else self.guest_name
        return f"{self.ticket_id} | {self.event.title} | {owner}"