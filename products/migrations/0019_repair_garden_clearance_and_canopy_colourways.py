from django.db import migrations
from django.db.models import Q


def repair_garden_clearance_and_canopy_colourways(apps, schema_editor):
    Product = apps.get_model('products', 'Product')

    Product.objects.filter(pk=49).update(
        category_id=4,
        collection_id=3,
        is_clearance=True,
    )
    Product.objects.filter(name__iexact='May Blossom Garden Bistro Set').update(
        category_id=4,
        collection_id=3,
        is_clearance=True,
    )

    Product.objects.filter(pk=77).update(
        category_id=10,
        collection_id=3,
        colour_finish='Pale Cream, Linen Whisper, Peacock Teal, Sapphire Depth',
    )
    Product.objects.filter(name__iexact='The Garden Canopy Umbrella').update(
        category_id=10,
        collection_id=3,
        colour_finish='Pale Cream, Linen Whisper, Peacock Teal, Sapphire Depth',
    )

    umbrella_products = Product.objects.filter(
        Q(name__icontains='umbrella') | Q(name__icontains='canopy')
    )
    umbrella_products.update(
        category_id=10,
        collection_id=3,
    )

    colour_names = (
        'Pale Cream',
        'Linen Whisper',
        'Peacock Teal',
        'Sapphire Depth',
    )
    for product in umbrella_products:
        if product.colour_finish:
            continue

        searchable_text = f'{product.name} {product.description}'.lower()
        matched_colours = [
            colour for colour in colour_names
            if colour.lower() in searchable_text
        ]
        if matched_colours:
            product.colour_finish = ', '.join(matched_colours)
            product.save(update_fields=['colour_finish'])


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_repair_garden_canopy_catalog'),
    ]

    operations = [
        migrations.RunPython(
            repair_garden_clearance_and_canopy_colourways,
            migrations.RunPython.noop,
        ),
    ]
