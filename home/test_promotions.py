from django.test import TestCase
from django.urls import reverse

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
