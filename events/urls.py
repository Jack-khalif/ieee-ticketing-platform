from django.urls import path
from . import views

urlpatterns = [
    # 1. Matches: http://127.0.0.1:8000/api/events/
    path('', views.EventListAPIView.as_view(), name='list-events'),
    
    # 2. Matches: http://127.0.0.1:8000/api/events/create/
    path('create/', views.create_event, name='create-event'),
    #fecth a single event by its slug
    path('<slug:slug>/', views.EventDetailAPIView.as_view(), name='detail-event'),
    path('<int:pk>/update/', views.update_event, name='update_event'),
    path('delete-all/', views.delete_all_events, name='delete-all'),
    
]