from django.db import migrations


def rename_cloud_paper_blouse(apps, schema_editor):
    Product = apps.get_model('products', 'Product')

    Product.objects.filter(pk=76).update(
        name='Cloud Paper Cotton Blouse',
        description=(
            'A crisp white cotton blouse with a cinematic mirror portrait mood, '
            'added to Vintage Notes as a softly modern companion piece.'
        ),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_add_cloud_paper_cotton_top'),
    ]

    operations = [
        migrations.RunPython(
            rename_cloud_paper_blouse,
            migrations.RunPython.noop,
        ),
    ]
