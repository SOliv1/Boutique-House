from django.db import models


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
	is_active = models.BooleanField(default=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-updated_at']
		verbose_name = 'Home Hero'
		verbose_name_plural = 'Home Hero Entries'

	def __str__(self):
		status = 'active' if self.is_active else 'inactive'
		return f'{self.season_label} ({status})'
