from django.db import migrations, models
from django.db.models import Q


VINTAGE_NOTES_SEO = {
    'seo_title': 'Vintage Notes — Boutique House',
    'seo_description': (
        'A curated collection of vintage fashion and archival pieces with '
        'character, craftsmanship, and quiet beauty.'
    ),
    'seo_keywords': (
        'vintage fashion uk, collectors edition clothing, '
        'boutique house vintage, curated vintage'
    ),
}

EMBER_GARDEN_SEO = {
    'seo_title': 'Ember Garden — Boutique House',
    'seo_description': (
        'Seasonal homeware and curated garden pieces inspired by warmth, '
        'texture, and outdoor living.'
    ),
    'seo_keywords': (
        'garden decor uk, curated homeware, boutique house interiors'
    ),
}


def seed_seo_copy(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    Collection = apps.get_model('products', 'Collection')

    Collection.objects.filter(name='vintage_notes').update(**VINTAGE_NOTES_SEO)
    Collection.objects.filter(name='garden').update(**EMBER_GARDEN_SEO)

    Product.objects.filter(name__iexact='Elephant Motif A-Line Skirt').update(
        seo_title='Elephant Motif A-Line Skirt — Boutique House',
        seo_description=(
            '1978 collectors-edition A-line skirt with hand-stitched elephant '
            'appliqué. A one-of-a-kind vintage piece from Boutique House.'
        ),
        seo_keywords=(
            'vintage skirt, elephant motif skirt, 1978 vintage fashion, '
            'collectors edition skirt, boutique house vintage'
        ),
    )
    Product.objects.filter(
        collection__name='vintage_notes',
    ).filter(
        Q(name__icontains='cerulean')
        | Q(description__icontains='cerulean'),
    ).update(
        seo_description=(
            'Soft cerulean vintage top from 1978 with a relaxed, feminine fit. '
            'Complements the Elephant Motif Skirt.'
        ),
        seo_keywords=(
            'cerulean top, vintage blouse 1978, collectors edition top, '
            'boutique house vintage'
        ),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_vintage_notes_menu_categories_and_munich_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='seo_description',
            field=models.CharField(
                blank=True,
                help_text='Short factual search and social description.',
                max_length=320,
            ),
        ),
        migrations.AddField(
            model_name='collection',
            name='seo_keywords',
            field=models.CharField(
                blank=True,
                help_text='Comma-separated search phrases.',
                max_length=500,
            ),
        ),
        migrations.AddField(
            model_name='collection',
            name='seo_title',
            field=models.CharField(
                blank=True,
                help_text=(
                    'Browser and search title. Leave blank to use the '
                    'collection name.'
                ),
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='seo_description',
            field=models.CharField(
                blank=True,
                help_text=(
                    'Short factual, keyword-aware search and social description.'
                ),
                max_length=320,
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='seo_keywords',
            field=models.CharField(
                blank=True,
                help_text='Comma-separated product search phrases.',
                max_length=500,
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='seo_title',
            field=models.CharField(
                blank=True,
                help_text=(
                    'Browser and search title. Leave blank to use Product '
                    'Name — Boutique House.'
                ),
                max_length=255,
            ),
        ),
        migrations.RunPython(seed_seo_copy, migrations.RunPython.noop),
    ]
