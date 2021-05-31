from django.conf import settings


def cart_contents(request):

    items = []
    total = 0
    product_count = 0
    delivery = 0

    if total > 0:
        delivery = (total * settings.DELIVERY_SURCHARGE) - total

    grand_total = total * delivery
    
    context = {
        'items': items,
        'total': total,
        'grand_total': grand_total,
        'product_count': product_count,
        'delivery': delivery,
    }  

    return context