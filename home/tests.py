from datetime import date
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from .models import HomePageHero
from .seasonal_covers import SeasonalCover, get_seasonal_cover


class HomePageTests(TestCase):
    @mock.patch('home.views.get_seasonal_cover')
    def test_home_page_returns_200(self, mock_get_seasonal_cover):
        mock_get_seasonal_cover.return_value = SeasonalCover(
            season='summer',
            label='Summer Edit',
            path='images/collections/seasonal/boutique-bannerSummer.png',
            url='/static/images/collections/seasonal/boutique-bannerSummer.png',
        )

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'images/collections/seasonal/boutique-bannerSummer.png',
        )

    def test_home_page_renders_mobile_navigation_drawer(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, 'class="bh-mobile-menu-toggle')
        self.assertContains(response, 'id="main-nav"')
        self.assertContains(response, 'class="bh-drawer-close"')
        self.assertContains(response, 'class="bh-drawer-backdrop')
        self.assertNotContains(response, "includes/main-nav.html")

    def test_home_page_uses_admin_portrait_url(self):
        portrait_url = 'https://images.example.com/model-portrait.jpg'
        HomePageHero.objects.create(
            portrait_image_url=portrait_url,
            is_active=True,
        )

        response = self.client.get(reverse('home'))

        self.assertContains(response, portrait_url)


class SeasonalCoverTests(TestCase):
    def test_august_final_week_prepares_autumn_cover(self):
        cover = get_seasonal_cover(current_date=date(2026, 8, 31))

        self.assertEqual(cover.season, 'autumn')
        self.assertEqual(cover.label, 'Autumn Edit')

    def test_seasonal_cover_falls_back_until_image_is_added(self):
        with mock.patch('home.seasonal_covers.finders.find') as mock_find:
            mock_find.return_value = None
            cover = get_seasonal_cover(current_date=date(2026, 8, 31))

        self.assertEqual(
            cover.path,
            'images/collections/garden/boutique-banner-portrait.png',
        )
