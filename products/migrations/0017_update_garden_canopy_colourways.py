from django.db import migrations


GARDEN_CANOPY_IMAGE = (
    'https://res.cloudinary.com/dwpvbtoad/image/upload/'
    'v1781559221/linen-whisper-saphire-depth_yf8zfw.png'
)


def update_garden_canopy_colourways(apps, schema_editor):
    Product = apps.get_model('products', 'Product')

    Product.objects.filter(pk=77).update(
        category_id=10,
        collection_id=3,
        colour_finish='Linen Whisper, Sapphire Depth',
        image_url=GARDEN_CANOPY_IMAGE,
    )
    Product.objects.filter(name__iexact='Garden Canopy Umbrella').update(
        category_id=10,
        collection_id=3,
        colour_finish='Linen Whisper, Sapphire Depth',
        image_url=GARDEN_CANOPY_IMAGE,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_update_vintage_notes_colourways'),
    ]

    operations = [
        migrations.RunPython(
            update_garden_canopy_colourways,
            migrations.RunPython.noop,
        ),
    ]
