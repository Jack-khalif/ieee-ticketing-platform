from django.urls import path
from . import views

urlpatterns = [
    # 1. Matches: http://127.0.0.1:8000/api/events/
    path('', views.EventListAPIView.as_view(), name='list-events'),
    
    # 2. Matches: http://127.0.0.1:8000/api/events/create/
    path('create/', views.create_event, name='create-event'),
]