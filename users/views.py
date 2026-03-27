from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def register_user(request):
    # Grab the data from the React form
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    # Basic validation
    if not username or not password:
        return Response({"error": "Username and password are required!"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "That username is already taken."}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user and their unique Token
    user = User.objects.create_user(username=username, email=email, password=password)
    token, created = Token.objects.get_or_create(user=user)

    # Send the token back to React!
    return Response({
        "token": token.key, 
        "user_id": user.id, 
        "username": user.username
    }, status=status.HTTP_201_CREATED)