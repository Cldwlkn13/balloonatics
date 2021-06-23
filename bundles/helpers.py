from django.http import HttpResponse

from products.models import Product
from cart.helpers import custom_formset_dictionary_parser

from decimal import Decimal

import math


def get_total_price(request):
    reqDict = request.body.decode("utf-8").split('&')
    bundle_item_dict = custom_formset_dictionary_parser(reqDict)
    total = 0
    for item in bundle_item_dict.values():
        if not item['product'] == '0':
            product = Product.objects.get(
                pk=item['product'])
            item_total = Decimal(item['item_qty']) * product.discounted_price
            total += item_total

    total = math.ceil(total) - 0.01

    return HttpResponse(content=total, status=200)


def validate_bundle_items(bundle_items):
    total = 0
    for item in bundle_items:
        product = Product.objects.get(pk=item.product.id)
        qty_held = product.qty_held
        if item.item_qty > qty_held:
            item.item_qty = qty_held
            item.item_cost = product.discounted_price * item.item_qty
        total += item.item_cost
    
    total = math.ceil(total) - 0.01

    return [bundle_items, total]


