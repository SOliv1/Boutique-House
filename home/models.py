from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class HomePageHero(models.Model):
	season_label = models.CharField(max_length=80, default='Summer Edit')
	heading = models.CharField(
		max_length=140,
		default='The new collections are here',
	)
	subheading = models.TextField(
		default='Soft, sculptural, editorial. A quiet, modern counterpoint that keeps the UI clean.',
	)
	cta_label = models.CharField(max_length=40, default='Shop Now')
	portrait_image = models.ImageField(
		upload_to='hero/',
		blank=True,
		null=True,
	)
	portrait_image_url = models.URLField(
		blank=True,
		help_text='Recommended on Railway: use a permanent hosted image URL.',
	)
	is_active = models.BooleanField(default=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-updated_at']
		verbose_name = 'Home Hero'
		verbose_name_plural = 'Home Hero Entries'

	def __str__(self):
		status = 'active' if self.is_active else 'inactive'
		return f'{self.season_label} ({status})'


class HomePromotion(models.Model):
	eyebrow = models.CharField(
		max_length=80,
		default='The After-Dark Collection',
	)
	heading = models.CharField(
		max_length=140,
		default='Candlelight, composed',
	)
	body = models.TextField(
		default=(
			'Discover our evening mood: sculptural candlelight, rich plum '
			'tones and beautifully considered objects.'
		),
	)
	cta_label = models.CharField(
		max_length=50,
		default='Discover the collection',
	)
	cta_url = models.CharField(
		max_length=500,
		default='/products/?collection=moods_board',
		help_text='Use a site path or a complete URL.',
	)
	terms_text = models.CharField(
		max_length=180,
		blank=True,
		default='A Boutique House mood story.',
	)
	promotion_image = models.ImageField(
		upload_to='promotions/',
		blank=True,
		null=True,
	)
	promotion_image_url = models.URLField(
		blank=True,
		help_text='Recommended on Railway: use a permanent hosted image URL.',
	)
	theme_color = models.CharField(
		max_length=7,
		default='#604858',
		help_text='Hex colour used for the button and decorative details.',
		validators=[
			RegexValidator(
				r'^#[0-9A-Fa-f]{6}$',
				'Enter a six-digit hex colour such as #604858.',
			),
		],
	)
	delay_seconds = models.PositiveSmallIntegerField(
		default=4,
		help_text='How long to wait before opening the promotion.',
	)
	dismiss_for_days = models.PositiveSmallIntegerField(
		default=14,
		help_text='How long a visitor dismissal should be remembered.',
	)
	is_active = models.BooleanField(default=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-updated_at']
		verbose_name = 'Home Promotion'
		verbose_name_plural = 'Home Promotions'

	def __str__(self):
		status = 'active' if self.is_active else 'inactive'
		return f'{self.heading} ({status})'

	def clean(self):
		super().clean()
		if not (
			self.cta_url.startswith('/')
			or self.cta_url.startswith('https://')
			or self.cta_url.startswith('http://')
		):
			raise ValidationError({
				'cta_url': 'Use a site path beginning with / or a full URL.',
			})
