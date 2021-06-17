from django.http import HttpResponse

from products.models import Product
from cart.helpers import custom_formset_dictionary_parser

from decimal import Decimal


def serve_image(request, product_id):
    product = Product.objects.get(pk=product_id)
    
    if not product:
        return HttpResponse(content='../media/noimage.png', status=400)

    return HttpResponse(content=product.image.url, status=200)


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

    return HttpResponse(content=total, status=200)


