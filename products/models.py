from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Collection(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    hero_image_url = models.CharField(max_length=1024, null=True, blank=True)
    hero_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    collection = models.ForeignKey('Collection', null=True, blank=True,
                                   on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    product_family = models.CharField(max_length=254, null=True, blank=True)
    colour_finish = models.CharField(max_length=254, null=True, blank=True)
    stock_quantity = models.PositiveIntegerField('total stock', default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)
    is_new_arrival = models.BooleanField(default=False)
    is_special_offer = models.BooleanField(default=False)
    is_clearance = models.BooleanField(default=False)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True,
                                 blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def available_stock(self):
        return max(self.stock_quantity - self.reserved_quantity, 0)

