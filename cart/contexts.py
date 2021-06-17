from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from bundles.models import Bundle, BundleItem
from printing.models import CustomPrintOrder
from decimal import Decimal


def cart_contents(request):

    cart_items = []
    total = 0
    product_count = 0
    delivery = 0.00
    cart = request.session.get('cart', {'products':{},'bundles':{},'custom_prints':{}})
    
    for i, q in cart['products'].items():
        item_total = 0
        product = get_object_or_404(Product, pk=i)
        item_total = q * product.discounted_price
        total += item_total
        product_count += q
        cart_items.append({
            'type': 'product',
            'item_id': i,
            "qty": q,
            'product': product,
            'item_total': item_total,
        })
    
    for i, q in cart['bundles'].items():
        bundle = Bundle.objects.get(bundle_id=i)
        bundle_items = BundleItem.objects.filter(bundle__bundle_id=i)

        d = {}
        for item in bundle_items:
            d[item.product.name] = item.item_qty

        bundle_total_cost = q * bundle.total_cost
        if(bundle_total_cost > 0):
            total = Decimal(bundle_total_cost) + Decimal(total)

        cart_items.append({
            'type': 'bundle',
            'item_id': i,
            "qty": q,
            'bundle_items': d,
            'bundle': bundle,
            'bundle_total_cost': bundle_total_cost,
        })
    
    for i, q in cart['custom_prints'].items():
        item_total = 0
        custom_print_order = get_object_or_404(CustomPrintOrder, pk=i)
        item_total = round(((int(q) * Decimal(custom_print_order.base_product.discounted_price))
                        * Decimal(settings.PRINTING_SURCHARGE)),2)
        total += item_total
        product_count += q
        cart_items.append({
            'type': 'custom_print',
            'item_id': i,
            "qty": q,
            'custom_print_order': custom_print_order,
            'item_total': item_total,
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
