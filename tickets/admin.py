# tickets/admin.py
from django.contrib import admin
from .models import Ticket
from .tasks import send_ticket_email

@admin.action(description="Send ticket email")
def send_email(modeladmin, request, queryset):
    for ticket in queryset:
        send_ticket_email(ticket)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "buyer", "price", "checked_in")
    actions = [send_email]