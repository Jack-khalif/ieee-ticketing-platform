from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    capacity = models.IntegerField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='posters/', null=True, blank=True)

    def __str__(self):
        return self.title
    
'''
models.Model → this tells Django “this is a blueprint for a table in the database.”

Each attribute (title, description, etc.) → a column in the table.

__str__ → how this object will appear in the admin dashboard (like the display name of a department)
'''