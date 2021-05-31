from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from decimal import Decimal

import math 


def cart_contents(request):

    cart_items = []
    total = 0
    product_count = 0
    delivery = 0.00
    cart = request.session.get('cart', {})

    for i, q in cart.items():
        item_total = 0
        product = get_object_or_404(Product, pk=i)
        item_total = q * product.discounted_price
        total += item_total
        product_count += q
        cart_items.append({
            'item_id': i,
            "qty": q,
            'product': product,
            'item_total': item_total,
        })
        print(total)
    
    if total > 0:
        delivery = round((total * Decimal(
            settings.DELIVERY_SURCHARGE)), 2)

    grand_total = total + delivery

    context = {
        'cart_items': cart_items,
        'total': total,
        'grand_total': grand_total,
        'product_count': product_count,
        'delivery': delivery,
    }

    return context
