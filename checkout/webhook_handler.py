from django.http import HttpResponse

from .models import Order
from .emails import send_order_confirmation

import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        send_order_confirmation(order)

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event['data']['object']
        pid = intent.id

        for attempt in range(5):
            try:
                order = Order.objects.get(stripe_pid=pid)
            except Order.DoesNotExist:
                if attempt < 4:
                    time.sleep(1)
                continue

            self._send_confirmation_email(order)
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    'SUCCESS: Order confirmed'
                ),
                status=200,
            )

        return HttpResponse(
            content=(
                f'Webhook received: {event["type"]} | '
                f'ERROR: Order with payment ID {pid} was not found'
            ),
            status=500,
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
