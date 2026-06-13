from django.contrib import admin
from django.utils.html import format_html

from .models import HomePageHero


@admin.register(HomePageHero)
class HomePageHeroAdmin(admin.ModelAdmin):
    list_display = ('season_label', 'is_active', 'updated_at', 'image_preview')
    list_filter = ('is_active',)
    search_fields = ('season_label', 'heading')
    readonly_fields = ('updated_at', 'image_preview')

    fieldsets = (
        (
            'Hero Content',
            {
                'fields': (
                    'season_label',
                    'heading',
                    'subheading',
                    'cta_label',
                    'portrait_image',
                    'image_preview',
                    'is_active',
                    'updated_at',
                )
            },
        ),
    )

    @admin.display(description='Preview')
    def image_preview(self, obj):
        if obj and obj.portrait_image:
            return format_html(
                '<img src="{}" style="width: 96px; height: 120px; object-fit: cover; border-radius: 4px;" />',
                obj.portrait_image.url,
            )
        return 'No image'
