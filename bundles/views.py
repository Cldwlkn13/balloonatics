from django.shortcuts import (render,reverse, redirect)
from django.contrib import messages
from django.forms import formset_factory

from .models import Bundle, BundleItem
from .forms import BundleSelectorForm, BundleBuilderForm
from .helpers import validate_bundle_items

from products.models import Product


def bundle_categories(request):
    selector_form = BundleSelectorForm()

    slideshow_images = {
        'graduation-bundle.jpg': 'Our #1 Graduation Bundle',
        'Wedding_Bundle.png': 'Our #1 Wedding Bundle',
        'happy-21stbundle.jpg': 'Happy 21st!',
    }
    
    context = {
        'selector_form': selector_form,
        'slideshow_images': slideshow_images,
    }

    return render(request, 'bundles/bundles.html', context)


def bundles(request):
    if request.method == 'POST':

        category = request.POST['categories']
        age = None
        bundles = None

        if request.POST['age']:
            age = request.POST['age']
            bundles = Bundle.objects.filter(
                category=category, age=age)

        bundles = Bundle.objects.filter(category=category)
        selector_form = BundleSelectorForm(request.POST)

        context = {
            'selector_form': selector_form,
            'bundles': bundles,
        }

        return render(request, 'bundles/bundles.html', context)

    return redirect(reverse('bundle_categories'))


def with_items(request, bundle_id):

    bundle_items = BundleItem.objects.filter(
        bundle__bundle_id=bundle_id)

    if not bundle_items:
        messages.error(request, 
                      'Could not retrieve bundle items',
                      extra_tags='render_toast')
        return redirect(reverse('bundle_categories'))

    # get the adjusted bundle items from the request
    adjusted_bundle = validate_bundle_items(bundle_items)
    bundle_items = adjusted_bundle[0]
    adj_total_cost = adjusted_bundle[1]

    # get the bundle and the total cost 
    bundle = bundle_items[0].bundle
    bundle.total_cost = adj_total_cost
    
    # init the formset
    BundleBuilderFormset = formset_factory(
        BundleBuilderForm, extra=0)
    
    # load up the formset with the data from the bundle
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






