from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField

from decimal import Decimal

from products.models import Product
from profiles.models import UserProfile
from bundles.models import Bundle
from printing.models import CustomPrintOrder

from validators import *

import uuid


class Address(models.Model):

    class Meta:
        verbose_name_plural = 'Addresses'

    street_address_1 = models.CharField(
        max_length=100, null=False, blank=False)
    street_address_2 = models.CharField(
        max_length=100, null=True, blank=True)
    city_town = models.CharField(
        max_length=20, null=False, blank=False)
    county_area = models.CharField(
        max_length=40, null=False, blank=False)
    country = CountryField(
       blank_label='Country *', null=False, blank=False)
    postal_code = models.CharField(
        max_length=10, null=True, blank=True)

    def __init__from_profile(self, userprofile):
        self.street_address_2 = userprofile.street_address_1
        if userprofile.street_address_2:
            self.street_address_2 = userprofile.street_address_2
        self.city_town = userprofile.city_town
        self.county_area = userprofile.county_area
        self.country = userprofile.country
        if userprofile.postal_code:
            self.postal_code = userprofile.postal_code
  
    def __str__(self):
        
        address = []
        address.append(self.street_address_1)
        address.append(", ")
        if self.street_address_2:
            address.append(self.street_address_2)
            address.append(", ")
        address.append(self.city_town)
        address.append(", ")
        address.append(self.county_area)
        address.append(", ")
        address.append(str(self.country))
        if self.postal_code:
            address.append(", ")
            address.append(self.postal_code)

        return ''.join(address)


class Order(models.Model):
    
    order_id = models.CharField(max_length=56, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    cust_name = models.CharField(max_length=50, null=False, blank=False, 
        validators=[alpha])
    cust_email = models.EmailField(max_length=254, null=False, blank=False)
    cust_phone = models.CharField(max_length=20, null=False, blank=False,
        validators=[numeric])
    date = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, null=False, blank=True,
                                on_delete=models.CASCADE,
                                related_name='address')
    delivery_surcharge = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0.00)
    items_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0.00)
    grand_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0.00)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')

    def __str__(self):
        return self.order_id

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self._generate_order_number()
        self.address.save()
        super().save(*args, **kwargs)

    def calc_grand_total(self):
        self.items_total = self.order_items.aggregate(
            Sum('item_total'))['item_total__sum'] or 0
        self.delivery_surcharge = (
            round((self.items_total * Decimal(
                  settings.DELIVERY_SURCHARGE)), 2))
        self.grand_total = self.delivery_surcharge + self.items_total
        self.save()


class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, null=False, blank=True,
                              on_delete=models.CASCADE,
                              related_name='order_items')

    product = models.ForeignKey(Product, null=True, blank=True,
                                on_delete=models.SET_NULL)
    bundle = models.ForeignKey(Bundle, null=True, blank=True,
                                on_delete=models.SET_NULL)
    
    custom_print_order = models.ForeignKey(CustomPrintOrder, 
                                null=True, blank=True,
                                on_delete=models.SET_NULL)

    order_item_id = models.CharField(max_length=32, null=False, editable=False)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    item_total = models.DecimalField(max_digits=6, decimal_places=2,
        null=False, default=0.00, editable=False)


    def __str__(self):
        return self.order_item_id

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        if not self.order_item_id:
            self.order_item_id = self._generate_order_number()
        if self.product:
            self.item_total = (
                self.product.discounted_price * self.quantity)
        elif self.bundle:
            self.item_total = (
                self.bundle.total_cost * self.quantity)
        elif self.custom_print_order:
            item_total = (Decimal(
                self.custom_print_order.base_product.discounted_price)
                 * int(self.quantity))
            self.item_total = (item_total * Decimal(settings.PRINTING_SURCHARGE))
        else:
            self.item_total = 0
        super().save(*args, **kwargs)

