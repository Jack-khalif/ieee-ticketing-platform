from django.urls import path
from . import views

urlpatterns = [
    # Matches: http://127.0.0.1:8000/api/tickets/purchase/
    path('purchase/', views.purchase_tickets, name='purchase_tickets'),
    path('scan/', views.scan_ticket, name='scan_ticket'),
    path('dashboard/<int:event_id>/', views.event_dashboard, name='event_dashboard'),
    path('dashboard/<int:event_id>/blast/', views.send_event_blast, name='send_event_blast'),
]