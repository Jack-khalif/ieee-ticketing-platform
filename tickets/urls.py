from django.urls import path
from .views import TicketPurchaseAPIView,ScanTicketAPIView,ValidateTicketAPIView

urlpatterns = [
    path('tickets/buy/', TicketPurchaseAPIView.as_view(), name='ticket-buy'),
    path('tickets/scan/',ScanTicketAPIView.as_view(), name='ticket-scan'),
    path('tickets/validate/',ValidateTicketAPIView.as_view(),name='ticket-validate'),
]