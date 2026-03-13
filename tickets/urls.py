from django.urls import path
from .views import TicketPurchaseAPIView,ScanTicketAPIView,ValidateTicketAPIView,verify_ticket,scanner_page

urlpatterns = [
    path('tickets/buy/', TicketPurchaseAPIView.as_view(), name='ticket-buy'),
    path('tickets/scan/',ScanTicketAPIView.as_view(), name='ticket-scan'),
    path('tickets/validate/',ValidateTicketAPIView.as_view(),name='ticket-validate'),
    path("verify-ticket/<int:ticket_id>/", verify_ticket),
    path("scanner/", scanner_page),
    
]