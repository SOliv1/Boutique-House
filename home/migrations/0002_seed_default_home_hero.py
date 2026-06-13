from django.db import migrations, models


def seed_default_home_hero(apps, schema_editor):
    HomePageHero = apps.get_model('home', 'HomePageHero')

    has_any = HomePageHero.objects.exists()
    if has_any:
        return

    HomePageHero.objects.create(
        season_label='Summer Edit',
        heading='The new collections are here',
        subheading='Soft, sculptural, editorial. A quiet, modern counterpoint that keeps the UI clean.',
        cta_label='Shop Now',
        is_active=True,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagehero',
            name='portrait_image_url',
            field=models.URLField(
                blank=True,
                help_text=(
                    'Recommended on Railway: use a permanent hosted image URL.'
                ),
            ),
        ),
        migrations.RunPython(seed_default_home_hero, migrations.RunPython.noop),
    ]
