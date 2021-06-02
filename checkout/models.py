from django.db import models
from django.db.models import Sum
from django.conf import settings

from products.models import Product

import uuid


class Address(models.Model):

    street_address_1 = models.CharField(
        max_length=100, null=False, blank=False)
    street_address_2 = models.CharField(
        max_length=100, null=True, blank=True)
    city_town = models.CharField(
        max_length=20, null=False, blank=False)
    county_area = models.CharField(
        max_length=20, null=False, blank=False)
    country = models.CharField(
        max_length=20, null=False, blank=False)
    postal_code = models.CharField(
        max_length=10, null=True, blank=True)

    def __str__(self):
        address = (self.street_address_1 + '\n' +
                   self.street_address_2 + '\n' +
                   self.city_town + '\n' +
                   self.county_area + '\n' +
                   self.country)

        if self.postal_code:
            address = address + '\n' + self.postal_code

        return address


class Order(models.Model):

    order_id = models.CharField(max_length=56, null=False, editable=False)
    cust_name = models.CharField(max_length=50, null=False, blank=False)
    cust_email = models.EmailField(max_length=254, null=False, blank=False)
    cust_phone = models.CharField(max_length=20, null=False, blank=False)
    address = models.ForeignKey(Address, null=False, blank=False,
                                on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    delivery_surcharge = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0.00)
    items_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0.00)
    grand_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0.00)

    def __str__(self):
        return str(self.cust_name).replace(" ", "") + self.order_id

    def produce_shipping_label(self):
        return (self.cust_name + '\n' + str(self.address))

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self._generate_order_number()
        super().save(*args, **kwargs)

    def calc_grand_total(self):
        self.order_total = self.order_items.aggregrate(
            Sum('order_item_total'))['order_item_total__sum']
        self.delivery_surcharge = (
            self.order_total * settings.DELIVERY_SURCHARGE)
        self.grand_total = self.delivery_surcharge + self.order_total
        self.save()


class OrderItem(models.Model):

    order = models.ForeignKey(Order, null=False, blank=True,
                              on_delete=models.CASCADE,
                              related_name='order_items')
    product = models.ForeignKey(Product, null=False, blank=True,
                                on_delete=models.CASCADE)
    order_item_id = models.CharField(max_length=32, null=False, editable=False)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    item_total = models.DecimalField(
        max_digits=6, decimal_places=2,
        null=False, default=0.00, editable=False)

    def __str__(self):
        return self.order_item_id + '_' + self.product.id

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        if not self.order_item_id:
            self.order_item_id = self._generate_order_number()
        self.item_total = (
            self.product.discounted_price * self.quantity)
        super().save(*args, **kwargs)


