from django.urls import path
from .views import TicketPurchaseAPIView

urlpatterns = [
    path('tickets/buy/', TicketPurchaseAPIView.as_view(), name='ticket-buy'),
]