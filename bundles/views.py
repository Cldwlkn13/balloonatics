from django.shortcuts import (render, HttpResponse,
                              reverse, redirect)

from .models import Bundle
from .forms import BundleFormset, BundleSelectorForm
from products.models import Product


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

    return redirect(reverse('bundlecategories'))


def with_items(request, bundle_id):
    bundle = Bundle.objects.get(pk=bundle_id)
    formset = BundleFormset()

    products = Product.objects.all()
    product_names = [(p.id, p.name) for p in products]
    for form in formset.forms:
        form.fields['product'].choices = product_names

    context = {
        'bundle': bundle,
        'formset': formset
    }

    return render(request, 'bundles/with_items.html', context)


def serve_image(request, product_id):
    product = Product.objects.get(pk=product_id)
    if not product:
        return HttpResponse(content='noimage.png', status=400)
    return HttpResponse(content=product.image.url, status=200)
