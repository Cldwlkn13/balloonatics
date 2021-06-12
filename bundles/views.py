from django.shortcuts import (render, HttpResponse,
                              reverse, redirect)

from .models import Bundle, BundleItem
from .forms import BundleSelectorForm, BundleBuilderForm
from products.models import Product
from django.forms import formset_factory


def bundle_categories(request):
    selector_form = BundleSelectorForm()

    context = {
        'selector_form': selector_form,
    }

    return render(request, 'bundles/bundles.html', context)


def bundles(request):
    if request.method == 'POST':

        category = request.POST['categories']
        age = None
        bundles = None

        if request.POST['age']:
            age = request.POST['age']
            bundles = Bundle.objects.filter(category=category, age=age)

        bundles = Bundle.objects.filter(category=category)
        selector_form = BundleSelectorForm(request.POST)

        context = {
            'selector_form': selector_form,
            'bundles': bundles,
        }

        return render(request, 'bundles/bundles.html', context)

    return redirect(reverse('bundle_categories'))


def with_items(request, bundle_id):
    if request.method == 'POST':

        context = {}
        
        return render(request, 'bundles/with_items.html', context)

    bundle = Bundle.objects.get(bundle_id=bundle_id)
    bundle_items = list(BundleItem.objects.filter(
        bundle__bundle_id=bundle_id))
    
    BundleBuilderFormset = formset_factory(
        BundleBuilderForm, extra=0)
    
    formset = BundleBuilderFormset(
        initial=[{
            'product': item.product.pk, 
            'item_qty': item.item_qty 
            } for item in bundle_items])

    context = {
        'bundle': bundle,
        'formset': formset
    }

    return render(request, 'bundles/with_items.html', context)


def serve_image(request, product_id):
    product = Product.objects.get(pk=product_id)
    
    if not product:
        return HttpResponse(content='../media/noimage.png', status=400)

    return HttpResponse(content=product.image.url, status=200)
