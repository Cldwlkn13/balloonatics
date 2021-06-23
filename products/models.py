from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from decimal import Decimal


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
    full_price = models.DecimalField(max_digits=6, decimal_places=2, blank=False,
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
    image = models.ImageField(null=True, blank=True)
    message = models.CharField(max_length=254, null=True, blank=True)
    is_printable = models.BooleanField(default=False)
    age = models.PositiveIntegerField(null=True, blank=True)
    color = models.ForeignKey('Color', null=True, blank=True,
                              on_delete=models.SET_NULL)
    size = models.ForeignKey('Size', null=True, blank=True,
                             on_delete=models.SET_NULL)
    # How many do we have in stock?                          
    qty_held = models.PositiveIntegerField(default=0) 
    shipped_inflated = models.BooleanField(default=False)
    qty_in_bag = models.PositiveIntegerField(default=0) #remove and use annotation


    def __str__(self):
        return self.name

    def calc_qty_in_bag(self, cart):
        if str(self.pk) in cart['products']:
            return cart['products'][str(self.pk)]
        else:
            return 0




