from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    # 1. Matches: http://127.0.0.1:8000/api/users/signup/
    path('signup/', views.register_user, name='signup'),
    
    # 2. Matches: http://127.0.0.1:8000/api/users/login/
    # (obtain_auth_token is a magic built-in DRF view that handles passwords for us!)
    path('login/', obtain_auth_token, name='login'), 
]