from django.db import models

from products.models import Product

import uuid


class Bundle(models.Model):
    bundle_id = models.CharField(max_length=56, null=True, editable=False)
    name = models.CharField(max_length=254, null=False, blank=False)

    def __str__(self):
        return self.bundle_id

    def _generate_bundle_id(self):
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        if not self.bundle_id:
            self.bundle_id = self._generate_bundle_id()
        super().save(*args, **kwargs)


class BundleItem(models.Model):
    bundle = models.ForeignKey(Bundle, null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name='bundle_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                null=True,
                                blank=True)

    def __str__(self):
        return self.product.name
