from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _


@shared_task
def reset_password(context):
    subject = _(f'Password reset')

    html_message = render_to_string('user/password-reset-email.html', {'email': context['email'],
                                                                       'protocol': context['protocol'],
                                                                       'domain': context['domain'],
                                                                       'uid': context['uid'],
                                                                       'token': context['token']})
    plain_message = strip_tags(html_message)

    msg = EmailMultiAlternatives(subject, plain_message, settings.EMAIL_HOST_USER, [context['email']])
    msg.attach_alternative(html_message, "text/html")
    msg.send()
    return msg


@shared_task
def contact_created(data):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    subject = _('Feedback from {email}, {name}').format(
        email=data['email'],
        name=data['name']
    )
    message = data['message']
    mail_sent = send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER]
    )
    return mail_sent
