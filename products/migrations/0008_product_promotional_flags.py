from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_collection_hero_image_collection_hero_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_clearance',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='is_new_arrival',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='is_special_offer',
            field=models.BooleanField(default=False),
        ),
    ]
