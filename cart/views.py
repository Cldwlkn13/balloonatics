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
    this_url = request.META['HTTP_REFERER']

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
    this_url = request.META['HTTP_REFERER']
    qty = int(request.POST.get('qty'))

    if request.POST.get('qty') == '':
        messages.error(request, 'Invalid quantity', '')
        return redirect(this_url)

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

    if 'cart' in this_url:
        extra_tags = ''

    messages.info(
        request,
        f'Updated cart with {qty} x <strong>{product.name}</strong>!',
        extra_tags=extra_tags)

    request.session['cart'] = cart
    return redirect(this_url)


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
    
    this_url = request.META['HTTP_REFERER']
    cart = request.session.get('cart', {})

    orig_bundle_pk = int(request.POST.get('orig_bundle_pk'))
    orig_bundle = get_object_or_404(Bundle, pk=orig_bundle_pk)

    # generate new bundle for this instance
    my_bundle_id = uuid.uuid4().hex.upper() 
    my_bundle = Bundle(
        bundle_id=my_bundle_id,
        name='My Custom ' + orig_bundle.name,
        image=orig_bundle.image,
        category=BundleCategory.objects.get(name='custom'),
        custom=True,
    )
    my_bundle.save()

    # get the customised bundle items of the request
    reqDict = request.body.decode("utf-8").split('&')
    bundle_item_dict = custom_formset_dictionary_parser(reqDict)

    canProcess = validate_bundle_item_qty(bundle_item_dict)
    if not canProcess[0]:
        messages.error(request, 
                    getCannotProcessMessage(canProcess[1]),
                    extra_tags='render_toast')
        return redirect(this_url)

    save_bundle_items(bundle_item_dict, my_bundle)
    
    cart[my_bundle_id] = 1 # handle qtys here

    messages.success(
        request,
        f'Added your bundle to your cart!',
        extra_tags='render_toast render_preview')
    
    request.session['cart'] = cart

    return redirect('bundle_categories')

def update_bundle_in_cart(request, bundle_id):
    
    this_url = request.META['HTTP_REFERER']
    my_bundle = get_object_or_404(Bundle, bundle_id=bundle_id)

    reqDict = request.body.decode("utf-8").split('&')
    bundle_item_dict = custom_formset_dictionary_parser(reqDict)
  
    canProcess = validate_bundle_item_qty(bundle_item_dict)
    if not canProcess[0]:
        messages.error(request, 
                    getCannotProcessMessage(canProcess[1]),
                    extra_tags='render_toast')
        return redirect(this_url)

    # if canProcess the update then lets delete the current items in the bundle and replace them all 
    BundleItem.objects.filter(
        bundle__bundle_id=bundle_id).delete()
    
    save_bundle_items(bundle_item_dict, my_bundle)

    cart = request.session.get('cart', {})
    cart[bundle_id] = 1
    extra_tags = 'render_toast render_preview'

    if 'cart' in this_url:
        extra_tags = ''

    messages.info(
        request,
        f'Updated cart for <strong>{my_bundle.name}</strong>!',
        extra_tags=extra_tags)

    request.session['cart'] = cart
    
    return redirect(this_url)


def remove_bundle_from_cart(request, bundle_id):
    
    bundle = get_object_or_404(Bundle, bundle_id=bundle_id)
    Bundle.objects.filter(bundle_id=bundle_id).delete()

    cart = request.session.get('cart', {})
    this_url = request.META['HTTP_REFERER']
    
    extra_tags = 'render_toast render_preview'

    if 'cart' in this_url:
        extra_tags = ''

    if bundle_id in cart:
        cart.pop(bundle_id)
        messages.info(
            request,
            f'<strong>{bundle.name}</strong> removed from your cart!',
            extra_tags=extra_tags)

    request.session['cart'] = cart
    
    return redirect(this_url)


def validate_bundle_item_qty(bundle_item_dict):
    for k, item in bundle_item_dict.items(): 
        if item['product'] != '0':
            product = Product.objects.get(pk=item['product'])
            if int(item['item_qty']) > product.qty_held:
                return [False, product]
    return [True, ]


def save_bundle_items(bundle_item_dict, my_bundle):
    for k, item in bundle_item_dict.items():
        if item['product'] != '0':
            product = Product.objects.get(pk=item['product'])
            bundle_item = BundleItem(
                product=product,
                bundle=my_bundle,
                item_qty=int(item['item_qty'])
            )
            bundle_item.save()


def getCannotProcessMessage(product):
    msg = ''
    if product.qty_held == 0:
        msg = f'''
        Sorry! We could not update your bundle. 
        We currently have no item <strong>{ product.name }</strong> 
        in stock!
        Please replace with another product.'''
    else:
        msg = f'''
        Sorry! We could not update your bundle. 
        The qty of item <strong>{ product.name }</strong> 
        is too high! 
        We only have { product.qty_held } in stock.'''
        
    return msg
            



