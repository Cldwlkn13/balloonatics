from django.http import HttpResponse
from django.conf import settings

from products.models import Product

from decimal import Decimal


def get_total_price(request):

    reqDict = request.body.decode("utf-8").split('&')
    
    try:
        p_id = custom_dictionary_parser(reqDict)['p_id']
        qty = custom_dictionary_parser(reqDict)['qty']
        product = Product.objects.get(pk=p_id)
        item_cost = Decimal(product.discounted_price) * int(qty)
        with_printing = round(item_cost * Decimal(
            settings.PRINTING_SURCHARGE),2)
    except Product.DoesNotExist:
        return HttpResponse(content=0, status=400)

    return HttpResponse(content=with_printing, status=200)


def custom_dictionary_parser(requestDictionary):
    d = {}
    for i in requestDictionary:
        k = i.split('=')[0]
        v = i.split('=')[1] 
        if 'csrf' not in k:    
            d[k] = v
    
    return d