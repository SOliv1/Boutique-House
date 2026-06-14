from django.test import TestCase
from django.urls import reverse

from checkout.models import Order, OrderLineItem
from products.models import Product

from .models import HomePromotion


class HomePromotionTests(TestCase):
    def setUp(self):
        HomePromotion.objects.all().delete()

    def test_active_promotion_renders_on_home_page(self):
        promotion = HomePromotion.objects.create(
            heading='Candlelight, composed',
            is_active=True,
        )

        response = self.client.get(reverse('home'))

        self.assertContains(response, promotion.heading)
        self.assertContains(response, 'The After-Dark Collection')
        self.assertContains(response, 'Discover the collection')
        self.assertContains(response, 'promotion-popup.js')
        self.assertContains(
            response,
            'boutique-house-cinematic-promotion.jpg',
        )

    def test_inactive_promotion_does_not_render(self):
        HomePromotion.objects.create(
            heading='Hidden promotion',
            is_active=False,
        )

        response = self.client.get(reverse('home'))

        self.assertNotContains(response, 'Hidden promotion')
        self.assertNotContains(response, 'id="home-promotion"')

    def test_privacy_policy_is_available_from_footer(self):
        home_response = self.client.get(reverse('home'))
        policy_response = self.client.get(reverse('privacy_policy'))

        self.assertContains(home_response, reverse('privacy_policy'))
        self.assertEqual(policy_response.status_code, 200)
        self.assertContains(policy_response, 'Privacy Policy')

    def test_terms_are_available_from_footer(self):
        home_response = self.client.get(reverse('home'))
        terms_response = self.client.get(reverse('terms_and_conditions'))

        self.assertContains(home_response, reverse('terms_and_conditions'))
        self.assertEqual(terms_response.status_code, 200)
        self.assertContains(terms_response, 'Terms &amp; Conditions')

    def test_delivery_and_tracking_are_available_from_footer(self):
        home_response = self.client.get(reverse('home'))
        delivery_response = self.client.get(reverse('delivery_information'))
        tracking_response = self.client.get(reverse('track_order'))

        self.assertContains(home_response, reverse('delivery_information'))
        self.assertContains(home_response, reverse('track_order'))
        self.assertContains(home_response, 'floating-order-tracker')
        self.assertEqual(delivery_response.status_code, 200)
        self.assertContains(delivery_response, 'Courier Delivery')
        self.assertEqual(tracking_response.status_code, 200)
        self.assertContains(tracking_response, 'Track Your Order')


class OrderTrackingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        product = Product.objects.create(
            name='Evening Glass Lantern',
            description='A softly lit lantern.',
            price='48.00',
        )
        cls.order = Order.objects.create(
            full_name='Sara Oliver',
            email='sara@example.com',
            phone_number='0123456789',
            country='GB',
            postcode='SW1A 1AA',
            town_or_city='London',
            street_address1='1 Boutique Lane',
            original_bag='{}',
            stripe_pid='pi_test',
        )
        OrderLineItem.objects.create(
            order=cls.order,
            product=product,
            quantity=1,
        )

    def test_matching_order_number_and_email_show_order(self):
        response = self.client.post(
            reverse('track_order'),
            {
                'order_number': self.order.order_number.lower(),
                'email': self.order.email.upper(),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.order_number)
        self.assertContains(response, 'Evening Glass Lantern')
        self.assertContains(response, 'We are preparing your order')

    def test_order_number_alone_does_not_reveal_order(self):
        response = self.client.post(
            reverse('track_order'),
            {
                'order_number': self.order.order_number,
                'email': 'someone-else@example.com',
            },
        )

        self.assertContains(response, 'could not find an order')
        self.assertNotContains(response, 'Evening Glass Lantern')
