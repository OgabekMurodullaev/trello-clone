from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_invite_email(workspace_name, email, accept_url, reject_url):
    subject = f"Ish maydoniga taklif"
    message = f"""
        Siz {workspace_name} ish maydoniga qo'shilish uchun taklif oldingiz!
        👉 Qabul qilish: {accept_url}
        ❌ Rad etish: {reject_url}"""
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])