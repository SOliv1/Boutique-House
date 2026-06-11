from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone


def send_order_confirmation(order):
    if order.confirmation_email_sent_at:
        return 0

    subject = render_to_string(
        'checkout/confirmation_emails/confirmation_email_subject.txt',
        {'order': order},
    ).strip()
    body = render_to_string(
        'checkout/confirmation_emails/confirmation_email_body.txt',
        {
            'order': order,
            'contact_email': settings.DEFAULT_FROM_EMAIL,
        },
    )

    messages_sent = send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
    )

    using_console_backend = settings.EMAIL_BACKEND.endswith(
        'console.EmailBackend'
    )
    if messages_sent and not using_console_backend:
        order.confirmation_email_sent_at = timezone.now()
        order.save(update_fields=['confirmation_email_sent_at'])

    return messages_sent
