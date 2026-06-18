from django.test import TestCase
from django.urls import reverse

from products.models import Product


class BagColourwayTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='The Garden Canopy Umbrella',
            description='A garden umbrella.',
            price='345.00',
            colour_finish='Linen Whisper, Sapphire Depth',
        )

    def test_colourways_are_stored_as_separate_bag_variants(self):
        add_url = reverse('add_to_bag', args=[self.product.id])

        self.client.post(add_url, {
            'quantity': 1,
            'product_colour': 'Linen Whisper',
            'redirect_url': reverse('product_detail', args=[self.product.id]),
        })
        self.client.post(add_url, {
            'quantity': 2,
            'product_colour': 'Sapphire Depth',
            'redirect_url': reverse('product_detail', args=[self.product.id]),
        })

        variants = self.client.session['bag'][str(self.product.id)]['items_by_variant']

        self.assertEqual(variants['no-size::Linen Whisper']['quantity'], 1)
        self.assertEqual(variants['no-size::Sapphire Depth']['quantity'], 2)


class BagActionTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Simple Bag Product',
            description='A product without size or colour variants.',
            price='25.00',
        )

    def _put_product_in_bag(self, quantity=1):
        session = self.client.session
        session['bag'] = {str(self.product.id): quantity}
        session.save()

    def test_adjusts_non_variant_product(self):
        self._put_product_in_bag()

        response = self.client.post(
            reverse('adjust_bag', args=[self.product.id]),
            {'quantity': 3},
        )

        self.assertRedirects(response, reverse('view_bag'))
        self.assertEqual(self.client.session['bag'][str(self.product.id)], 3)

    def test_removes_non_variant_product(self):
        self._put_product_in_bag()

        response = self.client.post(
            reverse('remove_from_bag', args=[self.product.id]),
        )

        self.assertRedirects(response, reverse('view_bag'))
        self.assertNotIn(str(self.product.id), self.client.session['bag'])

    def test_adjust_endpoint_rejects_direct_get(self):
        response = self.client.get(
            reverse('adjust_bag', args=[self.product.id]),
        )

        self.assertEqual(response.status_code, 405)
