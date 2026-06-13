from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_product_reserved_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='hero_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='collection',
            name='hero_image_url',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
