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
