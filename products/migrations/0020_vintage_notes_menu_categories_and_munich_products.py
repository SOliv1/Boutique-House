from django.db import migrations


VINTAGE_MENU_CATEGORIES = [
    ('early_sketch_collection', 'Early Sketch Collection'),
    ('timeless_dressing', 'Timeless Dressing'),
    ('worn_and_loved', 'Worn and Loved'),
    ('sketchbook', 'Sketchbook'),
    ('the_wardrobe', 'The Wardrobe'),
]

VINTAGE_PRODUCT_CATEGORY_UPDATES = {
    'BHVN-ES-001-LW': 'early_sketch_collection',
    'BHVN-ES-002-LW': 'timeless_dressing',
    'BHVN-ES-003-PC': 'worn_and_loved',
    'BHVN-TS-004-LW': 'sketchbook',
}

MUNICH_PRODUCTS = [
    {
        'sku': 'BHVN-TD-005-MB',
        'category': 'timeless_dressing',
        'product_family': 'TD-005',
        'colour_finish': 'Studio True, Sapphire Depth, Noir Shadow',
        'stock_quantity': 6,
        'reserved_quantity': 0,
        'is_new_arrival': True,
        'is_special_offer': False,
        'is_clearance': False,
        'is_coming_soon': False,
        'name': 'Munich Stripe Studio Blouse',
        'description': (
            'A blue striped button-through blouse with sculptural sleeves and a '
            'quiet gallery mood, styled for timeless dressing with clean black '
            'tailoring.'
        ),
        'has_sizes': True,
        'price': '118.00',
        'rating': '4.90',
        'image_url': '/static/images/products/vintage-notes/munich-timeless-dressing.png',
        'image': '',
    },
    {
        'sku': 'BHVN-WL-006-NS',
        'category': 'worn_and_loved',
        'product_family': 'WL-006',
        'colour_finish': 'Noir Shadow, Studio True',
        'stock_quantity': 6,
        'reserved_quantity': 0,
        'is_new_arrival': True,
        'is_special_offer': False,
        'is_clearance': False,
        'is_coming_soon': False,
        'name': 'Munich Worn Leather Mini Skirt',
        'description': (
            'A softly polished black leather mini skirt, made to feel already '
            'loved: simple, confident, and easy to wear with archive shirting.'
        ),
        'has_sizes': True,
        'price': '132.00',
        'rating': '4.90',
        'image_url': '/static/images/products/vintage-notes/munich-timeless-dressing.png',
        'image': '',
    },
]


def reset_sequence_for_model(schema_editor, model):
    table = model._meta.db_table
    pk_column = model._meta.pk.column
    vendor = schema_editor.connection.vendor

    with schema_editor.connection.cursor() as cursor:
        if vendor == 'postgresql':
            cursor.execute(
                "SELECT setval(pg_get_serial_sequence(%s, %s), "
                "COALESCE((SELECT MAX(id) FROM "
                + schema_editor.quote_name(table)
                + "), 1), true)",
                [table, pk_column],
            )
        elif vendor == 'sqlite':
            cursor.execute(
                "SELECT COALESCE(MAX(id), 0) FROM "
                + schema_editor.quote_name(table)
            )
            max_id = cursor.fetchone()[0]
            cursor.execute(
                "UPDATE sqlite_sequence SET seq = %s WHERE name = %s",
                [max_id, table],
            )


def reset_product_sequences(apps, schema_editor):
    for model_name in ('Category', 'Collection', 'Product'):
        reset_sequence_for_model(
            schema_editor,
            apps.get_model('products', model_name),
        )


def seed_vintage_notes_menu_categories(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    Product = apps.get_model('products', 'Product')
    Collection = apps.get_model('products', 'Collection')

    reset_product_sequences(apps, schema_editor)

    categories = {}
    for name, friendly_name in VINTAGE_MENU_CATEGORIES:
        category, _ = Category.objects.update_or_create(
            name=name,
            defaults={'friendly_name': friendly_name},
        )
        categories[name] = category

    vintage_collection = Collection.objects.filter(name='vintage_notes').first()
    if not vintage_collection:
        vintage_collection, _ = Collection.objects.update_or_create(
            name='vintage_notes',
            defaults={
                'friendly_name': 'Boutique House Vintage Notes',
                'description': (
                    'Timeless dressing, drawn from memory. Rediscovered from '
                    'original Boutique House sketches, c.1980-81.'
                ),
                'hero_image_url': (
                    '/static/images/products/vintage-notes/'
                    'munich-timeless-dressing.png'
                ),
                'hero_image': '',
            },
        )

    for sku, category_name in VINTAGE_PRODUCT_CATEGORY_UPDATES.items():
        Product.objects.filter(sku=sku).update(
            category=categories[category_name],
            collection=vintage_collection,
        )

    for product in MUNICH_PRODUCTS:
        fields = product.copy()
        sku = fields.pop('sku')
        category_name = fields.pop('category')
        fields['category'] = categories[category_name]
        fields['collection'] = vintage_collection
        Product.objects.update_or_create(
            sku=sku,
            defaults=fields,
        )

    reset_product_sequences(apps, schema_editor)


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_repair_garden_clearance_and_canopy_colourways'),
    ]

    operations = [
        migrations.RunPython(
            seed_vintage_notes_menu_categories,
            migrations.RunPython.noop,
        ),
    ]
