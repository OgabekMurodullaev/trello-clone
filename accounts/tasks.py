from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from accounts.models import User


@shared_task
def send_welcome_email_async(user_id):
    user = User.objects.get(id=user_id)
    subject = "Welcome to our platform!"
    message = f"Hello {user.first_name} {user.last_name}, welcome to our website!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
