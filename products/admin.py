from django.contrib import admin
from .models import Product, Category, Collection

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_per_page = 150
    list_max_show_all = 150

    list_display = (
        'sku',
        'name',
        'product_family',
        'colour_finish',
        'category',
        'collection',
        'stock_quantity',
        'reserved_quantity',
        'available_stock_display',
        'is_new_arrival',
        'is_special_offer',
        'is_clearance',
        'is_coming_soon',
        'price',
        'rating',
        'image',
    )
    list_filter = (
        'is_new_arrival',
        'is_special_offer',
        'is_clearance',
        'is_coming_soon',
        'product_family',
        'colour_finish',
        'category',
        'collection',
    )
    search_fields = ('sku', 'name', 'product_family', 'colour_finish')
    list_editable = (
        'stock_quantity',
        'reserved_quantity',
        'is_new_arrival',
        'is_special_offer',
        'is_clearance',
        'is_coming_soon',
        'price',
    )

    ordering = ('product_family', 'colour_finish', 'sku')

    @admin.display(description='Available stock')
    def available_stock_display(self, obj):
        return obj.available_stock


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)


class CollectionAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
        'hero_image',
        'hero_image_url',
    )


admin.site.register(Collection, CollectionAdmin)

