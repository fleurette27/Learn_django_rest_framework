from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Client, Staff

@api_view(['POST'])
def client_register(request):
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')
    address = request.data.get('address')

    if Client.objects.filter(email=email).exists():
        return Response({'error': 'Client with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    client = Client(email=email, username=username, address=address)
    client.set_password(password)
    client.save()
    return Response({'message': 'Client registered successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def client_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        client = Client.objects.get(email=email)
        if client.check_password(password):
            # Logique d'authentification réussie pour le client
            return Response({'message': 'Client logged in successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
    except Client.DoesNotExist:
        return Response({'error': 'Client does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def staff_register(request):
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')
    department = request.data.get('department')

    if Staff.objects.filter(email=email).exists():
        return Response({'error': 'Staff with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    staff = Staff(email=email, username=username, department=department)
    staff.set_password(password)
    staff.save()
    return Response({'message': 'Staff registered successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def staff_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        staff = Staff.objects.get(email=email)
        if staff.check_password(password):
            # Logique d'authentification réussie pour le staff
            return Response({'message': 'Staff logged in successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
    except Staff.DoesNotExist:
        return Response({'error': 'Staff does not exist'}, status=status.HTTP_404_NOT_FOUND)


# authapp/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Client, Staff

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_client_info(request):
    user = request.user  # Supposons que l'utilisateur est déjà authentifié
    try:
        client = Client.objects.get(email=user.email)
        client.username = request.data.get('username', client.username)
        client.address = request.data.get('address', client.address)
        client.save()
        return Response({'message': 'Client information updated successfully'}, status=status.HTTP_200_OK)
    except Client.DoesNotExist:
        return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_staff_info(request):
    user = request.user  # Supposons que l'utilisateur est déjà authentifié
    try:
        staff = Staff.objects.get(email=user.email)
        staff.username = request.data.get('username', staff.username)
        staff.department = request.data.get('department', staff.department)
        staff.save()
        return Response({'message': 'Staff information updated successfully'}, status=status.HTTP_200_OK)
    except Staff.DoesNotExist:
        return Response({'error': 'Staff not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user  # Utilisateur authentifié
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    # Vérification de l'ancien mot de passe
    if user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)



from django.core.mail import send_mail
from django.utils.crypto import get_random_string

@api_view(['POST'])
def send_verification_email(request):
    email = request.data.get('email')
    user = Client.objects.filter(email=email).first() or Staff.objects.filter(email=email).first()
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




from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

@api_view(['GET'])
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Client.objects.get(pk=uid) or Staff.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Client.DoesNotExist, Staff.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # Active le compte
        user.save()
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid verification link'}, status=status.HTTP_400_BAD_REQUEST)


