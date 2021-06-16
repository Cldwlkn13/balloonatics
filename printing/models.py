from django.db import models

from products.models import Product


class CustomPrintedProduct(Product):
    custom_message = models.CharField(
        max_length=40, blank=False, null=False)

    def __str__(self):
        return self.name