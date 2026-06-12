from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Order


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
    @patch('checkout.views.send_order_confirmation')
    def test_confirmation_is_sent_in_production(
        self,
        send_order_confirmation,
    ):
        response = self.client.get(
            reverse(
                'checkout_success',
                args=[self.order.order_number],
            )
        )

        self.assertEqual(response.status_code, 200)
        send_order_confirmation.assert_called_once_with(self.order)
