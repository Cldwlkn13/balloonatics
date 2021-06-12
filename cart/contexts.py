from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from bundles.models import Bundle, BundleItem
from decimal import Decimal


def cart_contents(request):

    cart_items = []
    total = 0
    product_count = 0
    delivery = 0.00
    cart = request.session.get('cart', {})

    for i, q in cart.items():
        if len(i) < 32:
            item_total = 0
            product = get_object_or_404(Product, pk=i)
            item_total = q * product.discounted_price
            total += item_total
            product_count += q
            cart_items.append({
                'is_bundle': False,
                'item_id': i,
                "qty": q,
                'product': product,
                'item_total': item_total,
            })
        else:
            bundle = Bundle.objects.get(bundle_id=i)
            bundle_items = BundleItem.objects.filter(bundle__bundle_id=i)

            d = {}
            for item in bundle_items:
                d[item.product.name] = item.item_qty

            bundle_total_cost = q * bundle.total_cost
            if(bundle_total_cost > 0):
                total = Decimal(bundle_total_cost) + Decimal(total)

            cart_items.append({
                'is_bundle': True,
                'item_id': i,
                "qty": q,
                'bundle_items': d,
                'bundle': bundle,
                'bundle_total_cost': bundle_total_cost,
            })
           
    if total > 0:
        delivery = round((total * Decimal(
            settings.DELIVERY_SURCHARGE)), 2)

    grand_total = Decimal(total) + Decimal(delivery)

    context = {
        'cart_items': cart_items,
        'total': total,
        'grand_total': grand_total,
        'product_count': product_count,
        'delivery': delivery,
    }

    return context
