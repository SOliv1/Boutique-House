from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from .models import Order
from .webhook_handler import StripeWH_Handler


class CheckoutSuccessTests(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            full_name='Jane Doe',
            email='jane@example.com',
            phone_number='01234567890',
            country='GB',
            postcode='SW1A 1AA',
            town_or_city='London',
            street_address1='1 Example Street',
            original_bag='{}',
            stripe_pid='pi_test',
        )

    @override_settings(DEBUG=False)
    def test_success_page_renders_in_production(self):
        response = self.client.get(
            reverse(
                'checkout_success',
                args=[self.order.order_number],
            )
        )

        self.assertEqual(response.status_code, 200)


class PaymentIntentWebhookTests(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            full_name='Jane Doe',
            email='jane@example.com',
            phone_number='01234567890',
            country='GB',
            postcode='SW1A 1AA',
            town_or_city='London',
            street_address1='1 Example Street',
            original_bag='{}',
            stripe_pid='pi_test',
        )
        self.handler = StripeWH_Handler(RequestFactory().post('/checkout/wh/'))
        self.event = {
            'type': 'payment_intent.succeeded',
            'data': {
                'object': SimpleNamespace(id='pi_test'),
            },
        }

    @patch('checkout.webhook_handler.send_order_confirmation')
    def test_existing_order_is_confirmed(self, send_confirmation):
        response = self.handler.handle_payment_intent_succeeded(self.event)

        self.assertEqual(response.status_code, 200)
        send_confirmation.assert_called_once_with(self.order)
