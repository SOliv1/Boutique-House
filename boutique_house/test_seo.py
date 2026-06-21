from django.test import TestCase, override_settings
from django.urls import reverse

from products.models import Collection, Product


class PrototypeRobotsTests(TestCase):
    @override_settings(SEO_INDEXING_ENABLED=False)
    def test_prototype_blocks_all_crawlers(self):
        response = self.client.get(reverse('robots_txt'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertContains(response, 'User-agent: *')
        self.assertContains(response, 'Disallow: /')
        self.assertNotContains(response, 'Sitemap:')

    @override_settings(SEO_INDEXING_ENABLED=False)
    def test_prototype_pages_emit_noindex(self):
        response = self.client.get(reverse('home'))

        self.assertContains(
            response,
            '<meta name="robots" content="noindex, nofollow" />',
            html=True,
        )


class LaunchRobotsTests(TestCase):
    @override_settings(
        SEO_INDEXING_ENABLED=True,
        PUBLIC_SITE_URL='https://example.com',
    )
    def test_launch_rules_advertise_sitemap_and_protect_private_paths(self):
        response = self.client.get(reverse('robots_txt'))

        self.assertContains(response, 'Allow: /')
        self.assertContains(response, 'Disallow: /checkout/')
        self.assertContains(response, 'Sitemap: https://example.com/sitemap.xml')

    @override_settings(SEO_INDEXING_ENABLED=True)
    def test_private_pages_remain_noindex_after_launch(self):
        response = self.client.get(reverse('view_bag'))

        self.assertContains(
            response,
            '<meta name="robots" content="noindex, nofollow" />',
            html=True,
        )


class SitemapTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        collection = Collection.objects.create(
            name='sitemap_collection',
            friendly_name='Sitemap Collection',
        )
        cls.product = Product.objects.create(
            collection=collection,
            name='Sitemap Product',
            description='A sitemap test product.',
            price='25.00',
        )

    def test_sitemap_contains_public_product_and_collection_urls(self):
        response = self.client.get('/sitemap.xml')

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            reverse('product_detail', args=[self.product.pk]),
        )
        self.assertContains(
            response,
            '?collection=sitemap_collection',
        )
        self.assertNotContains(response, '/checkout/')
