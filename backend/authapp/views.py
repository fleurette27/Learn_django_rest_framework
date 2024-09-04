from django.shortcuts import render
# authapp/views.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import UserSerializer, LoginSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.mail import send_mail
from django.utils.crypto import get_random_string




@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_detail(request):
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)




@api_view(['POST'])
def send_verification_email(request):
    email = request.data.get('email')
    user = User.objects.filter(email=email).first()
    if user:
        verification_code = get_random_string(length=32)  # Génère un code de vérification unique
        user.verification_code = verification_code  # Stocke le code dans l'utilisateur (à supposer que tu as un champ pour ça)
        user.save()
        send_mail(
            'Verify Your Email Address',
            f'Your verification code is {verification_code}',
            'noreply@yourdomain.com',
            [email],
            fail_silently=False,
        )
        return Response({'message': 'Verification email sent successfully'}, status=status.HTTP_200_OK)
    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# authapp/views.py

@api_view(['GET'])
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid) 
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # Active le compte
        user.save()
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid verification link'}, status=status.HTTP_400_BAD_REQUEST)


