from django.db import models
from django.db.models import Sum
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

from products.models import Product

from decimal import Decimal

import uuid


class BundleCategory(models.Model):
    class Meta:
        verbose_name_plural = 'BundleCategories'
  
    name = models.CharField(max_length=254, blank=False, null=False)
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Bundle(models.Model):
    bundle_id = models.CharField(max_length=254, editable=False)
    name = models.CharField(max_length=254, null=False, blank=False)
    total_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                     blank=False, default=0.00,
                                     validators=[MinValueValidator(
                                      Decimal('0.00'))])
    category = models.ForeignKey(BundleCategory, on_delete=models.CASCADE,
                                 blank=False, null=False)
    age = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    custom = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
            null=True, blank=True)

    def __str__(self):
        return self.name

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def save(self, user_id=None, *args, **kwargs):
        if not self.bundle_id:
            self.bundle_id = self._generate_order_number()
        if not user_id == None:
            self.user = User.objects.get(pk=user_id)
        super().save(*args, **kwargs)

    def calc_bundle_total(self):
        self.total_cost = self.bundle_items.aggregate(
            Sum('item_cost'))['item_cost__sum'] or 0
        self.save()


class BundleItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                null=True, blank=True)
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE,
                               null=True, blank=True,
                               related_name="bundle_items")
    item_qty = models.PositiveIntegerField(default=0)
    item_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                    blank=False, default=0.00,
                                    validators=[MinValueValidator(
                                      Decimal('0.00'))])

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.item_cost = (self.product.discounted_price *
                          self.item_qty)
        super().save(*args, **kwargs)

