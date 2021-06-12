from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from bundles.models import Bundle, BundleItem
from decimal import Decimal


def cart_contents(request):

    cart_items = []
    bundle_cart_items = []
    total = 0.00
    product_count = 0
    delivery = 0.00
    cart = request.session.get('cart', {})
    bundle_cart = request.session.get('bundle_cart', {})

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
    
    for i, q in bundle_cart.items():
        bundle = Bundle.objects.get(bundle_id=i)
        bundle_items = BundleItem.objects.filter(bundle__bundle_id=i)

        d = {}
        for item in bundle_items:
            d[item.product.pk] = item.item_qty

        bundle_total_cost = q * bundle.total_cost
        # total = bundle_total_cost + total
        bundle_cart_items.append({
            'item_id': i,
            "qty": q,
            'bundle_items': d,
            'bundle_total_cost': bundle_total_cost,
        })
    

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
