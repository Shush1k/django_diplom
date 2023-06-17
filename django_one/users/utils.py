from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from users.tasks import send_email


def send_verify_email(request, user):
    current_site = get_current_site(request)

    context = {
        'user': user,
        'domain': current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": default_token_generator.make_token(user),
    }
    subject = 'Verify email to get access'
    message = render_to_string(
        'registration/verify_email.html',
        context=context,
    )
    send_email.delay(subject, message, user.email)
