from django.db import migrations, models


def refresh_seeded_promotion_copy(apps, schema_editor):
    HomePromotion = apps.get_model('home', 'HomePromotion')
    HomePromotion.objects.filter(
        eyebrow='The Cinematic Edit',
    ).update(
        eyebrow='The After-Dark Collection',
    )
    HomePromotion.objects.filter(
        cta_label='Explore the edit',
    ).update(
        cta_label='Discover the collection',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_homepromotion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepromotion',
            name='eyebrow',
            field=models.CharField(
                default='The After-Dark Collection',
                max_length=80,
            ),
        ),
        migrations.AlterField(
            model_name='homepromotion',
            name='cta_label',
            field=models.CharField(
                default='Discover the collection',
                max_length=50,
            ),
        ),
        migrations.RunPython(
            refresh_seeded_promotion_copy,
            migrations.RunPython.noop,
        ),
    ]
