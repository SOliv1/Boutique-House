from django.db import migrations


CLOUD_PAPER_COTTON_TOP = {
    'pk': 76,
    'sku': 'BHVN-TS-004-LW',
    'product_family': 'TS-004',
    'colour_finish': 'Linen Whisper',
    'stock_quantity': 6,
    'reserved_quantity': 0,
    'is_new_arrival': True,
    'is_special_offer': False,
    'is_clearance': False,
    'is_coming_soon': False,
    'name': 'Cloud Paper Cotton Blouse',
    'description': (
        'A crisp white cotton blouse with a cinematic mirror portrait mood, added '
        'to Vintage Notes as a softly modern companion piece.'
    ),
    'has_sizes': True,
    'price': '98.00',
    'rating': '4.90',
    'image_url': '/static/images/products/vintage-notes/cloud-paper-cotton-top.png',
    'image': '',
}


def add_cloud_paper_cotton_top(apps, schema_editor):
    Product = apps.get_model('products', 'Product')

    fields = CLOUD_PAPER_COTTON_TOP.copy()
    pk = fields.pop('pk')
    fields['category_id'] = 11
    fields['collection_id'] = 4
    Product.objects.update_or_create(
        pk=pk,
        defaults=fields,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_seed_vintage_notes_catalog'),
    ]

    operations = [
        migrations.RunPython(
            add_cloud_paper_cotton_top,
            migrations.RunPython.noop,
        ),
    ]
