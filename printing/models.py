from django.db import models

from django.contrib.auth.models import User

from products.models import Product


class CustomPrintedProduct(models.Model):

    base_product = models.ForeignKey(Product, 
                        on_delete=models.CASCADE, 
                        related_name='custom_prints',
                        null=False, blank=False)

    user = models.ForeignKey(User,
                        on_delete=models.CASCADE, 
                        related_name='custom_prints', 
                        null=False, blank=False)
    
    custom_message = models.CharField(
        max_length=40, blank=False, null=False)

    qty = models.PositiveIntegerField(default=0)

    
    def __str__(self):
        return self.base_product.name
