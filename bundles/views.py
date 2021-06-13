from django.shortcuts import (render,reverse, redirect)
from django.core.validators import MaxValueValidator
from django.contrib import messages
from django.forms import formset_factory
from django.db.models import Sum

from .models import Bundle, BundleItem
from .forms import BundleSelectorForm, BundleBuilderForm

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

    return redirect(reverse('bundle_categories'))


def with_items(request, bundle_id):

    bundle_items = BundleItem.objects.filter(
        bundle__bundle_id=bundle_id)

    if not bundle_items:
        messages.error(request, 
                      'Could not retrieve bundle items',
                      extra_tags='render_toast')
        return redirect(reverse('bundle_categories'))

    adjusted_bundle = validate_bundle_items(bundle_items)
    bundle_items = adjusted_bundle[0]
    adj_total_cost = adjusted_bundle[1]

    bundle = bundle_items[0].bundle
    bundle.total_cost = adj_total_cost
    
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


def validate_bundle_items(bundle_items):
    total = 0
    for item in bundle_items:
        product = Product.objects.get(pk=item.product.id)
        qty_held = product.qty_held
        if item.item_qty > qty_held:
            item.item_qty = qty_held
            item.item_cost = product.discounted_price * item.item_qty
        total += item.item_cost
    
    return [bundle_items, total]



