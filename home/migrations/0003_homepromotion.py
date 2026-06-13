import django.core.validators
from django.db import migrations, models


def seed_default_promotion(apps, schema_editor):
    HomePromotion = apps.get_model('home', 'HomePromotion')
    if HomePromotion.objects.exists():
        return

    HomePromotion.objects.create(
        eyebrow='The Cinematic Edit',
        heading='Candlelight, composed',
        body=(
            'Discover our evening mood: sculptural candlelight, rich plum '
            'tones and beautifully considered objects.'
        ),
        cta_label='Explore the edit',
        cta_url='/products/?collection=moods_board',
        terms_text='A Boutique House mood story.',
        theme_color='#604858',
        delay_seconds=4,
        dismiss_for_days=14,
        is_active=True,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_seed_default_home_hero'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePromotion',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'eyebrow',
                    models.CharField(
                        default='The Cinematic Edit',
                        max_length=80,
                    ),
                ),
                (
                    'heading',
                    models.CharField(
                        default='Candlelight, composed',
                        max_length=140,
                    ),
                ),
                (
                    'body',
                    models.TextField(
                        default=(
                            'Discover our evening mood: sculptural candlelight, '
                            'rich plum tones and beautifully considered objects.'
                        ),
                    ),
                ),
                (
                    'cta_label',
                    models.CharField(
                        default='Explore the edit',
                        max_length=50,
                    ),
                ),
                (
                    'cta_url',
                    models.CharField(
                        default='/products/?collection=moods_board',
                        help_text='Use a site path or a complete URL.',
                        max_length=500,
                    ),
                ),
                (
                    'terms_text',
                    models.CharField(
                        blank=True,
                        default='A Boutique House mood story.',
                        max_length=180,
                    ),
                ),
                (
                    'promotion_image',
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to='promotions/',
                    ),
                ),
                (
                    'promotion_image_url',
                    models.URLField(
                        blank=True,
                        help_text=(
                            'Recommended on Railway: use a permanent hosted '
                            'image URL.'
                        ),
                    ),
                ),
                (
                    'theme_color',
                    models.CharField(
                        default='#604858',
                        help_text=(
                            'Hex colour used for the button and decorative '
                            'details.'
                        ),
                        max_length=7,
                        validators=[
                            django.core.validators.RegexValidator(
                                '^#[0-9A-Fa-f]{6}$',
                                (
                                    'Enter a six-digit hex colour such as '
                                    '#604858.'
                                ),
                            ),
                        ],
                    ),
                ),
                (
                    'delay_seconds',
                    models.PositiveSmallIntegerField(
                        default=4,
                        help_text=(
                            'How long to wait before opening the promotion.'
                        ),
                    ),
                ),
                (
                    'dismiss_for_days',
                    models.PositiveSmallIntegerField(
                        default=14,
                        help_text=(
                            'How long a visitor dismissal should be remembered.'
                        ),
                    ),
                ),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Home Promotion',
                'verbose_name_plural': 'Home Promotions',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.RunPython(
            seed_default_promotion,
            migrations.RunPython.noop,
        ),
    ]
