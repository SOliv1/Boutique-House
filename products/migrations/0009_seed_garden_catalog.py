import json
from pathlib import Path

from django.conf import settings
from django.db import migrations


def _load_fixture(name):
    fixture_path = (
        Path(settings.BASE_DIR) / 'products' / 'fixtures' / f'{name}.json'
    )
    with fixture_path.open(encoding='utf-8') as fixture:
        return json.load(fixture)


def seed_garden_catalog(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    Collection = apps.get_model('products', 'Collection')
    Product = apps.get_model('products', 'Product')

    for record in _load_fixture('categories'):
        Category.objects.update_or_create(
            pk=record['pk'],
            defaults=record['fields'],
        )

    for record in _load_fixture('collections'):
        Collection.objects.update_or_create(
            pk=record['pk'],
            defaults=record['fields'],
        )

    for record in _load_fixture('products'):
        if record['pk'] != 5 and record['pk'] < 40:
            continue

        fields = record['fields'].copy()
        fields['category_id'] = fields.pop('category')
        fields['collection_id'] = fields.pop('collection')
        Product.objects.update_or_create(
            pk=record['pk'],
            defaults=fields,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_product_promotional_flags'),
    ]

    operations = [
        migrations.RunPython(seed_garden_catalog, migrations.RunPython.noop),
    ]
