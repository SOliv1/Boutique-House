from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_repair_catalog_columns'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_coming_soon',
            field=models.BooleanField(default=False),
        ),
    ]
