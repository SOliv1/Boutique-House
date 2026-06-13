from django.contrib import admin
from django.utils.html import format_html

from .models import HomePageHero, HomePromotion


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
                    'portrait_image_url',
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
        if obj and (obj.portrait_image_url or obj.portrait_image):
            image_url = obj.portrait_image_url or obj.portrait_image.url
            return format_html(
                '<img src="{}" style="width: 96px; height: 120px; object-fit: cover; border-radius: 4px;" />',
                image_url,
            )
        return 'No image'


@admin.register(HomePromotion)
class HomePromotionAdmin(admin.ModelAdmin):
    list_display = ('heading', 'is_active', 'updated_at', 'image_preview')
    list_filter = ('is_active',)
    search_fields = ('eyebrow', 'heading', 'body')
    readonly_fields = ('updated_at', 'image_preview')

    fieldsets = (
        (
            'Promotion Content',
            {
                'fields': (
                    'eyebrow',
                    'heading',
                    'body',
                    'cta_label',
                    'cta_url',
                    'terms_text',
                )
            },
        ),
        (
            'Artwork and Appearance',
            {
                'fields': (
                    'promotion_image_url',
                    'promotion_image',
                    'image_preview',
                    'theme_color',
                )
            },
        ),
        (
            'Display Rules',
            {
                'fields': (
                    'delay_seconds',
                    'dismiss_for_days',
                    'is_active',
                    'updated_at',
                )
            },
        ),
    )

    @admin.display(description='Preview')
    def image_preview(self, obj):
        if obj and (obj.promotion_image_url or obj.promotion_image):
            image_url = obj.promotion_image_url or obj.promotion_image.url
            return format_html(
                '<img src="{}" style="width: 150px; height: 100px; '
                'object-fit: cover; border-radius: 4px;" />',
                image_url,
            )
        return 'Default Cinematic artwork'
