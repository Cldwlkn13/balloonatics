from django.shortcuts import HttpResponse
from django.conf import settings

from .models import Product

def serve_image(request, product_id):

    product = Product.objects.get(pk=product_id)
    
    if not product or not product.image:
        return HttpResponse(content=f'{settings.MEDIA_URL}noimage.png', status=200)

    return HttpResponse(content=product.image.url, status=200)