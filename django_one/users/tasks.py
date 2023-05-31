from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
# from django_one.celery import app


@shared_task
def send_feedback_email_task(email_address, message):
    """Sends an email when the feedback form has been submitted."""
    from time import sleep
    sleep(5)  # Simulate expensive operation(s) that freeze Django
    send_mail(
        "Your Feedback",
        f"\t{message}\n\nThank you!",
        settings.EMAIL_HOST_USER,
        [email_address],
        fail_silently=False,
    )
