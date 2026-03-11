from django.urls import path
from .views import InitiatePaymentAPIView, MpesaCallbackAPIView

urlpatterns = [
    path("initiate/", InitiatePaymentAPIView.as_view()),
    path("callback/", MpesaCallbackAPIView.as_view()),
]