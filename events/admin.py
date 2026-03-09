from django.contrib import admin

# Register your models here.
from .models import Event

admin.site.register(Event)

'''

You’re installing a control panel for this department
 in the admin dashboard. 
 Now you can manage events from Django admin.
'''