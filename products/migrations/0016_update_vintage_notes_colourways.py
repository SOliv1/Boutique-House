from django.db import migrations


def update_vintage_notes_colourways(apps, schema_editor):
    Product = apps.get_model('products', 'Product')

    Product.objects.filter(pk=75).update(
        colour_finish='Pale Cream, Ivory Silk, Noir Shadow, Rose Mist',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_rename_cloud_paper_blouse'),
    ]

    operations = [
        migrations.RunPython(
            update_vintage_notes_colourways,
            migrations.RunPython.noop,
        ),
    ]
