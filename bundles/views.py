from django.shortcuts import render, HttpResponse

#from .forms import BundleFormset
from products.models import Product


def bundles(request):
    #formset = BundleFormset()

    products = Product.objects.all()
    product_names = [(p.id, p.name) for p in products]
    #for form in formset.forms:
     #   form.fields['product'].choices = product_names

    context = {
        #'formset': formset
    }

    return render(request, 'bundles/bundles.html', context)


def serve_image(request, product_id):
    product = Product.objects.get(pk=product_id)
    if not product:
        return HttpResponse(content='noimage.png', status=400)
    return HttpResponse(content=product.image.url, status=200)
