from celery import shared_task
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from .models import CustomUser
from django.conf import settings

@shared_task
def send_password_reset_email(user_id, domain, email):
    user = CustomUser.objects.get(pk=user_id)
    token_generator = default_token_generator
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)

    reset_link = f"http://{domain}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"

    send_mail(
        subject='Password Reset Requested',
        message=f'Click the link to reset your password: {reset_link}',
        from_email=settings.EMAIL_HOST_USER,   
        recipient_list=[email],
        fail_silently=False,
    )
