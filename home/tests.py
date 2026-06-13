from django.test import TestCase
from django.urls import reverse

from .models import HomePageHero


class HomePageTests(TestCase):
    def test_home_page_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_admin_portrait_url(self):
        portrait_url = 'https://images.example.com/model-portrait.jpg'
        HomePageHero.objects.create(
            portrait_image_url=portrait_url,
            is_active=True,
        )

        response = self.client.get(reverse('home'))

        self.assertContains(response, portrait_url)
