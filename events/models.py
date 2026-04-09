import uuid
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    capacity = models.IntegerField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='posters/', null=True, blank=True)
    category = models.CharField(max_length=50, default='campus')

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not set
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Handle duplicate titles
            while Event.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def is_past(self):
        return self.date < timezone.now()

    def __str__(self):
        return self.title