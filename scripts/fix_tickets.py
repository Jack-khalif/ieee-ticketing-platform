from events.models import Event

Event.objects.create(
    title="Test Event",
    description="Temporary event for migration",
    location="Nairobi"
)