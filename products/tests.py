from django.test import TestCase
from django.urls import reverse

from .models import Category, Collection, Product


class GardenCollectionViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        garden_category, _ = Category.objects.update_or_create(
            name='garden',
            defaults={
                'friendly_name': 'Garden',
            },
        )
        cls.garden, _ = Collection.objects.update_or_create(
            name='garden',
            defaults={
                'friendly_name': 'The Garden Collection',
                'description': 'Outdoor pieces for slow mornings.',
                'hero_image_url': (
                    '/static/images/collections/garden/banner.png'
                ),
            },
        )
        Product.objects.create(
            category=garden_category,
            collection=cls.garden,
            name='Garden Lantern',
            description='An outdoor lantern.',
            price='46.00',
        )
        Product.objects.create(
            name='Indoor Vase',
            description='A decorative vase.',
            price='32.00',
        )

    def test_collection_filter_only_returns_garden_products(self):
        response = self.client.get(
            reverse('products'),
            {'collection': 'garden'},
        )

        self.assertContains(response, 'Garden Lantern')
        self.assertNotContains(response, 'Indoor Vase')
        self.assertEqual(response.context['current_collection'], self.garden)

    def test_collection_hero_content_is_rendered(self):
        response = self.client.get(
            reverse('products'),
            {'collection': 'garden'},
        )

        self.assertContains(response, 'The Garden Collection')
        self.assertContains(response, 'Outdoor pieces for slow mornings.')
        self.assertContains(response, self.garden.hero_image_url)


class ProductPromotionViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.collection, _ = Collection.objects.update_or_create(
            name='garden',
            defaults={
                'friendly_name': 'The Garden Collection',
            },
        )
        Product.objects.create(
            collection=cls.collection,
            name='New Garden Glasses',
            description='A new arrival.',
            price='75.00',
            is_new_arrival=True,
        )
        Product.objects.create(
            collection=cls.collection,
            name='Garden Deal',
            description='A special offer.',
            price='45.00',
            is_special_offer=True,
        )
        Product.objects.create(
            collection=cls.collection,
            name='Regular Garden Product',
            description='A standard product.',
            price='35.00',
        )

    def test_new_arrivals_filter_preserves_collection_membership(self):
        response = self.client.get(
            reverse('products'),
            {'promotion': 'new_arrivals'},
        )

        self.assertContains(response, 'New Garden Glasses')
        self.assertNotContains(response, 'Garden Deal')
        self.assertNotContains(response, 'Regular Garden Product')
        self.assertContains(response, 'New Arrivals')
        self.assertEqual(
            Product.objects.get(name='New Garden Glasses').collection,
            self.collection,
        )

    def test_special_deals_filter(self):
        response = self.client.get(
            reverse('products'),
            {'promotion': 'deals'},
        )

        self.assertContains(response, 'Garden Deal')
        self.assertNotContains(response, 'New Garden Glasses')
        self.assertContains(response, 'Special Deals')
