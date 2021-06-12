from bundles.forms import BundleBuilderFormset
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from products.models import Product
from bundles.models import Bundle, BundleItem, BundleCategory

from .helpers import custom_formset_dictionary_parser

import uuid


def view_cart(request):

    return render(request, 'cart/cart.html')


def add_product_to_cart(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    qty = int(request.POST.get('qty'))
    this_url = request.POST.get('this_url')

    if product.qty_held < qty:
        messages.warning(request,
                         'Sorry! We could add this item to your cart. '
                         'We do not have the required amount '
                         'in stock.',
                         extra_tags='render_toast')
        return redirect(this_url)

    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += qty
    else:
        cart[item_id] = qty

    messages.success(
        request,
        f'Added {qty} x <strong>{product.name}</strong> to your cart!',
        extra_tags='render_toast render_preview')

    request.session['cart'] = cart
    return redirect(this_url)


def update_product_cart(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    path = request.POST.get('this_url')
    qty = int(request.POST.get('qty'))

    if request.POST.get('qty') == '':
        messages.error(request, 'Invalid quantity', '')
        return redirect(path)

    if product.qty_held < qty:
        messages.warning(request,
                         'Sorry! We could not update this item '
                         'qty in your cart. '
                         'We do not have the required amount '
                         'in stock.',
                         extra_tags='render_toast')
        return redirect(path)

    cart = request.session.get('cart', {})
    cart[item_id] = qty
    extra_tags = 'render_toast render_preview'

    if 'cart' in path:
        extra_tags = ''

    messages.info(
        request,
        f'Updated cart with {qty} x <strong>{product.name}</strong>!',
        extra_tags=extra_tags)

    request.session['cart'] = cart
    return redirect(path)


def remove_product_from_cart(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    cart = request.session.get('cart', {})
    this_url = request.META['HTTP_REFERER']
    extra_tags = 'render_toast render_preview'

    if 'cart' in this_url:
        extra_tags = ''

    if item_id in cart:
        cart.pop(item_id)
        messages.info(
            request,
            f'<strong>{product.name}</strong> removed from your cart!',
            extra_tags=extra_tags)

    request.session['cart'] = cart
    return redirect(this_url)


def add_bundle_to_cart(request):
    
    bundle_cart = request.session.get('bundle_cart', {})

    bundle_pk = int(request.POST.get('orig_bundle_pk'))
    orig_bundle = get_object_or_404(Bundle, pk=bundle_pk)

    my_bundle_id = uuid.uuid4().hex.upper()

    reqDict = request.body.decode("utf-8").split('&')
    bundle_item_dict = custom_formset_dictionary_parser(reqDict)

    
    my_bundle = Bundle(
        bundle_id=my_bundle_id,
        name='My Custom ' + orig_bundle.name,
        category=BundleCategory.objects.get(name='custom'),
        custom=True
    )
    my_bundle.save()

    for k, item in bundle_item_dict.items():
        product = Product.objects.get(pk=item['product'])
        bundle_item = BundleItem(
            product=product,
            bundle=my_bundle,
            item_qty=int(item['item_qty'])
        )
        bundle_item.save()

    bundle_cart[my_bundle_id] = 1 # handle qtys here

    messages.success(
        request,
        f'Added your bundle to your cart!',
        extra_tags='render_toast render_preview')
    
    request.session['bundle_cart'] = bundle_cart 
    

    return redirect('bundle_categories')



