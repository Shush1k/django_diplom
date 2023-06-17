from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_email(subject, message, email):

    send_mail(
        subject,
        f"\t{message}\nСпасибо,\nКоманда разработчиков",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
