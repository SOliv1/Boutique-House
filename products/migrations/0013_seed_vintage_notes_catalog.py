from django.db import migrations


VINTAGE_CATEGORY = {
    'name': 'vintage_notes',
    'friendly_name': 'Vintage Notes',
}

VINTAGE_COLLECTION = {
    'name': 'vintage_notes',
    'friendly_name': 'Boutique House Vintage Notes',
    'description': (
        'Timeless dressing, drawn from memory. Rediscovered from original '
        'Boutique House sketches, c.1980-81.'
    ),
    'hero_image_url': '/static/images/products/vintage-notes/riviera-trouser-set.png',
    'hero_image': '',
}

VINTAGE_PRODUCTS = [
    {
        'pk': 73,
        'sku': 'BHVN-ES-001-LW',
        'product_family': 'ES-001',
        'colour_finish': 'Linen Whisper, Pale Cream, Soft Meadow',
        'stock_quantity': 6,
        'reserved_quantity': 0,
        'is_new_arrival': True,
        'is_special_offer': False,
        'is_clearance': False,
        'is_coming_soon': False,
        'name': 'Meadow Skirt Set',
        'description': (
            'Drawn from an original Boutique House sketch, c.1980-81. A '
            'countryside skirt set remembered from summers long ago, reimagined '
            'in quiet, softly worn colourways.'
        ),
        'has_sizes': True,
        'price': '128.00',
        'rating': '4.90',
        'image_url': '/static/images/products/vintage-notes/meadow-skirt-set.png',
        'image': '',
    },
    {
        'pk': 74,
        'sku': 'BHVN-ES-002-LW',
        'product_family': 'ES-002',
        'colour_finish': 'Linen Whisper, Oyster, Peacock Teal, Midnight Ink',
        'stock_quantity': 6,
        'reserved_quantity': 0,
        'is_new_arrival': True,
        'is_special_offer': False,
        'is_clearance': False,
        'is_coming_soon': False,
        'name': 'Riviera Trouser Set',
        'description': (
            'Drawn from an original Boutique House sketch, c.1980-81. Effortless '
            'wide-leg tailoring with a soft Riviera lightness, designed to '
            'outlast trends.'
        ),
        'has_sizes': True,
        'price': '148.00',
        'rating': '4.90',
        'image_url': '/static/images/products/vintage-notes/riviera-trouser-set.png',
        'image': '',
    },
    {
        'pk': 75,
        'sku': 'BHVN-ES-003-PC',
        'product_family': 'ES-003',
        'colour_finish': 'Pale Cream, Ivory Silk, Noir Shadow, Rose Mist',
        'stock_quantity': 6,
        'reserved_quantity': 0,
        'is_new_arrival': True,
        'is_special_offer': False,
        'is_clearance': False,
        'is_coming_soon': False,
        'name': 'Poet Skirt Ensemble',
        'description': (
            'Drawn from an original Boutique House sketch, c.1980-81. A romantic '
            'blouse and skirt ensemble inspired by favourite clothes, handwritten '
            'notes, and old light.'
        ),
        'has_sizes': True,
        'price': '136.00',
        'rating': '4.90',
        'image_url': '/static/images/products/vintage-notes/poet-skirt-ensemble.png',
        'image': '',
    },
]


def seed_vintage_notes_catalog(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    Collection = apps.get_model('products', 'Collection')
    Product = apps.get_model('products', 'Product')

    Category.objects.update_or_create(
        pk=11,
        defaults=VINTAGE_CATEGORY,
    )
    Collection.objects.update_or_create(
        pk=4,
        defaults=VINTAGE_COLLECTION,
    )

    for product in VINTAGE_PRODUCTS:
        fields = product.copy()
        pk = fields.pop('pk')
        fields['category_id'] = 11
        fields['collection_id'] = 4
        Product.objects.update_or_create(
            pk=pk,
            defaults=fields,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_product_is_coming_soon'),
    ]

    operations = [
        migrations.RunPython(
            seed_vintage_notes_catalog,
            migrations.RunPython.noop,
        ),
    ]
