from django.db import models
from django.conf import settings

from products.models import Product

from decimal import Decimal


class CustomPrintOrder(models.Model):

    base_product = models.ForeignKey(Product, 
                        on_delete=models.CASCADE, 
                        related_name='custom_prints', null=False,
                        blank=False)
    custom_message = models.CharField(
        max_length=40, blank=False, null=False)
    qty = models.PositiveIntegerField(default=0)
    total_cost = models.DecimalField(max_digits=6, decimal_places=2,
        null=False, default=0.00, editable=False)


    def __str__(self):
        return self.base_product.name


    def save(self, *args, **kwargs):
        self.total_cost = self.calc_total_cost()
        super().save(*args, **kwargs)

    
    def calc_total_cost(self):
        item_total = Decimal(self.base_product.discounted_price) * int(self.qty)
        return item_total * Decimal(settings.PRINTING_SURCHARGE)