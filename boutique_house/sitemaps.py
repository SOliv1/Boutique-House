from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from products.models import Collection, Product


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return (
            'home',
            'products',
            'delivery_information',
            'privacy_policy',
            'terms_and_conditions',
        )

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == 'home' else 0.5


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_coming_soon=False).order_by('pk')

    def location(self, product):
        return reverse('product_detail', args=[product.pk])


class CollectionSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Collection.objects.exclude(name='moods_board').order_by('pk')

    def location(self, collection):
        products_url = reverse('products')
        return f'{products_url}?collection={collection.name}'


sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'collections': CollectionSitemap,
}
