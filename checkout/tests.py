from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import RequestFactory, TestCase, override_settings
from django.utils import timezone
from django.urls import reverse

from .admin import OrderAdmin
from .models import Order, OrderLineItem
from .webhook_handler import StripeWH_Handler
from products.models import Product


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
        self.product = Product.objects.create(
            name='The Garden Canopy Umbrella',
            description='A garden umbrella.',
            price='345.00',
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

    @override_settings(DEBUG=False)
    def test_success_page_shows_selected_colourway(self):
        OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            product_colour='Sapphire Depth',
        )

        response = self.client.get(
            reverse(
                'checkout_success',
                args=[self.order.order_number],
            )
        )

        self.assertContains(response, 'Colour: Sapphire Depth')

    @override_settings(
        DEBUG=False,
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        DEFAULT_FROM_EMAIL='orders@boutique-house.test',
    )
    def test_success_page_sends_customer_confirmation_email(self):
        OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            product_colour='Sapphire Depth',
        )

        response = self.client.get(
            reverse(
                'checkout_success',
                args=[self.order.order_number],
            )
        )

        self.order.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.order.order_number, mail.outbox[0].subject)
        self.assertIn('Selected Colour: Sapphire Depth', mail.outbox[0].body)
        self.assertIsNotNone(self.order.confirmation_email_sent_at)

    @override_settings(
        DEBUG=False,
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        DEFAULT_FROM_EMAIL='orders@boutique-house.test',
    )
    def test_success_page_does_not_resend_existing_confirmation_email(self):
        self.order.confirmation_email_sent_at = timezone.now()
        self.order.save(update_fields=['confirmation_email_sent_at'])

        response = self.client.get(
            reverse(
                'checkout_success',
                args=[self.order.order_number],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)


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


class WarehouseAdminActionTests(TestCase):
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
        self.user = get_user_model().objects.create_superuser(
            username='warehouse-admin',
            email='warehouse@example.com',
            password='testpass123',
        )
        self.request = RequestFactory().post('/admin/checkout/order/')
        self.request.user = self.user
        self.order_admin = OrderAdmin(Order, AdminSite())

    def test_send_to_warehouse_records_staff_reference(self):
        with patch.object(self.order_admin, 'message_user'):
            self.order_admin.send_to_warehouse(
                self.request,
                Order.objects.filter(pk=self.order.pk),
            )

        self.order.refresh_from_db()

        self.assertEqual(self.order.warehouse_status, Order.WAREHOUSE_SENT)
        self.assertEqual(self.order.warehouse_sent_by, self.user)
        self.assertEqual(self.order.warehouse_sent_by_role, 'Superuser')
        self.assertIsNotNone(self.order.warehouse_sent_at)

    def test_single_order_warehouse_button_route_records_staff_reference(self):
        with patch.object(self.order_admin, 'message_user'):
            response = self.order_admin.send_single_order_to_warehouse(
                self.request,
                str(self.order.pk),
            )

        self.order.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.order.warehouse_status, Order.WAREHOUSE_SENT)
        self.assertEqual(self.order.warehouse_sent_by, self.user)
        self.assertEqual(self.order.warehouse_sent_by_role, 'Superuser')
        self.assertIsNotNone(self.order.warehouse_sent_at)

    def test_admin_change_page_shows_prominent_warehouse_button(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse('admin:checkout_order_change', args=[self.order.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Send to Warehouse / Delivery')
        self.assertContains(response, 'Action needed:')
        self.assertContains(response, 'Warehouse tel: 020 7946 0182')
        self.assertContains(response, 'Warehouse contact:')

    def test_admin_order_list_renders_warehouse_status(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('admin:checkout_order_changelist'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Needs sending')
