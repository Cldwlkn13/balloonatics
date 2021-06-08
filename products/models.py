from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from decimal import Decimal

import uuid


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name


class Material(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Sub_Category(models.Model):

    class Meta:
        verbose_name_plural = 'Sub_Categories'

    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name


class Product(models.Model):
    name = models.CharField(max_length=254, null=False, blank=False)
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    sub_category = models.ForeignKey('Sub_Category', null=True, blank=True,
                                     on_delete=models.SET_NULL)
    material = models.ForeignKey('Material', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    uuid = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False,
                                default=0.00, validators=[MinValueValidator(
                                    Decimal('0.00'))])
    discounted_price = models.DecimalField(max_digits=6, decimal_places=2,
                                           blank=False, default=0.00,
                                           validators=[MinValueValidator(
                                               Decimal('0.00'))])
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True,
                                 blank=True, validators=[MinValueValidator(
                                     Decimal('0.00')), MaxValueValidator(
                                         Decimal('5.00'))])
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    message = models.CharField(max_length=254, null=True, blank=True)
    message_editable = models.BooleanField(null=False, blank=False,
                                           default=False)
    age = models.PositiveIntegerField(null=True, blank=True)
    color = models.ForeignKey('Color', null=True, blank=True,
                              on_delete=models.SET_NULL)
    size = models.ForeignKey('Size', null=True, blank=True,
                             on_delete=models.SET_NULL)
    qty_held = models.PositiveIntegerField(null=False)
    shipped_inflated = models.BooleanField(null=False, blank=False,
                                           default=False)
    is_printable = models.BooleanField(null=False, blank=False, default=False)
    qty_in_bag = models.PositiveIntegerField(null=True, blank=True, default=0)
    is_bundle = models.BooleanField(null=False, blank=False, default=False)
    bundle_items = models.ManyToManyField("self", symmetrical=False)

    def __str__(self):
        return self.name

    def calc_qty_in_bag(self, cart):
        if str(self.pk) in cart:
            return cart[str(self.pk)]
        else:
            return 0

