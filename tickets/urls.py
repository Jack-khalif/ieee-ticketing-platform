from django.urls import path
from . import views

urlpatterns = [
    # Matches: http://127.0.0.1:8000/api/tickets/purchase/
    path('purchase/', views.purchase_tickets, name='purchase_tickets'),
]