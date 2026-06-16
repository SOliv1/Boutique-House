from django.db import migrations


GARDEN_CANOPY_DEFAULTS = {
    'category_id': 10,
    'collection_id': 3,
    'sku': 'BH-GDN-ACC-011',
    'product_family': 'Garden Umbrella',
    'colour_finish': 'Pale Cream, Linen Whisper, Peacock Teal, Sapphire Depth',
    'stock_quantity': 6,
    'reserved_quantity': 0,
    'is_new_arrival': True,
    'is_special_offer': False,
    'is_clearance': False,
    'is_coming_soon': False,
    'name': 'The Garden Canopy Umbrella',
    'description': (
        'A refined fringed garden umbrella designed to bring softness, shade, '
        'and timeless elegance to outdoor spaces. Available in Pale Cream, '
        'Linen Whisper, Peacock Teal, and Sapphire Depth.'
    ),
    'has_sizes': False,
    'price': '345.00',
    'rating': '5.00',
}

GARDEN_COLLECTION_DEFAULTS = {
    'friendly_name': 'The Garden Collection',
    'description': (
        'A luminous outdoor world of furniture, tableware, roses, textiles, '
        'lighting, and beautifully useful pieces. Colour and atmosphere flow '
        'through Impressionist, Seasonal, Weather, Morning, Afternoon, Evening, '
        'Cinematic, and Midnight moods.'
    ),
    'hero_image_url': '/static/images/collections/garden/boutique-banner-reclining-parasol.png',
}


def repair_garden_canopy_catalog(apps, schema_editor):
    Collection = apps.get_model('products', 'Collection')
    Product = apps.get_model('products', 'Product')

    Collection.objects.filter(pk=3).update(**GARDEN_COLLECTION_DEFAULTS)
    Collection.objects.filter(name='garden').update(**GARDEN_COLLECTION_DEFAULTS)

    product, _ = Product.objects.update_or_create(
        pk=77,
        defaults=GARDEN_CANOPY_DEFAULTS,
    )

    if not product.image_url and not product.image:
        product.image_url = (
            'https://res.cloudinary.com/dwpvbtoad/image/upload/'
            'v1781559221/linen-whisper-saphire-depth_yf8zfw.png'
        )
        product.save(update_fields=['image_url'])


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_update_garden_canopy_colourways'),
    ]

    operations = [
        migrations.RunPython(
            repair_garden_canopy_catalog,
            migrations.RunPython.noop,
        ),
    ]
