from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_order_confirmation_email_sent_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderlineitem',
            name='product_colour',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
