from django.urls import path
from .views import InitiatePaymentAPIView, ConfirmPaymentAPIView

urlpatterns = [
    path('payments/initiate/', InitiatePaymentAPIView.as_view()),
    path('payments/confirm/', ConfirmPaymentAPIView.as_view()),
]