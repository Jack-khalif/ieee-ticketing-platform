from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # These are the columns that will show up in the Django Admin table
    list_display = ('ticket_id', 'event', 'get_buyer', 'purchase_date', 'is_scanned')
    
    # Adds a filter sidebar to quickly find scanned vs unscanned tickets
    list_filter = ('is_scanned', 'event')
    
    # Adds a search bar at the top!
    search_fields = ('ticket_id', 'guest_name', 'guest_email', 'user__username', 'event__title')

    # A quick helper function to show either the logged-in username OR the guest name
    def get_buyer(self, obj):
        if obj.user:
            return obj.user.username
        return f"{obj.guest_name} (Guest)"
    get_buyer.short_description = 'Buyer' # Names the column