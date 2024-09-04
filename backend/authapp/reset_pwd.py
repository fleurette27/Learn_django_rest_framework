# authapp/views.py
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Client, Staff
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


@api_view(['POST'])
def request_password_reset(request):
    email = request.data.get('email')
    user = Client.objects.filter(email=email).first() or Staff.objects.filter(email=email).first()

    if user:
        # Génère un jeton de réinitialisation
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Génère l'URL de réinitialisation
        reset_url = f"http://yourdomain.com/reset-password/{uid}/{token}/"

        # Envoie un e-mail à l'utilisateur
        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_url}',
            'noreply@yourdomain.com',
            [email],
            fail_silently=False,
        )
        return Response({'message': 'Password reset email sent successfully'}, status=status.HTTP_200_OK)
    
    return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Client.objects.get(pk=uid) if Client.objects.filter(pk=uid).exists() else Staff.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Client.DoesNotExist, Staff.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        new_password = request.data.get('new_password')
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid or expired reset link'}, status=status.HTTP_400_BAD_REQUEST)

