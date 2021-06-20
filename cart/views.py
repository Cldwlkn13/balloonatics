from django.shortcuts import (render, redirect, 
                              get_object_or_404,
                              HttpResponse)
from django.contrib import messages

from .helpers import custom_formset_dictionary_parser

from products.models import Product
from bundles.models import Bundle, BundleItem, BundleCategory
from printing.models import CustomPrintOrder

import uuid


def view_cart(request):

    return render(request, 'cart/cart.html')


def add_product_to_cart(request, item_id):
      
    referred_from = request.META['HTTP_REFERER']

    cart = request.session.get('cart', {'products':{},'bundles':{},'custom_prints':{}})
    
    product = get_object_or_404(Product, pk=item_id)
    qty = int(request.POST.get('qty'))

    if product.qty_held < qty:
        messages.warning(request,
                         'Sorry! We could add this item to your cart. '
                         'We do not have the required amount '
                         'in stock.',
                         extra_tags='render_toast')
        return redirect(referred_from)

    if item_id in list(cart['products'].keys()):
        cart['products'][item_id] += qty
    else:
        cart['products'][item_id] = qty

    messages.success(
        request,
        f'Added {qty} x <strong>{product.name}</strong> to your cart!',
        extra_tags='render_toast render_preview')

    request.session['cart'] = cart
    return redirect(referred_from)


def update_product_cart(request, item_id):
    
    product = get_object_or_404(Product, pk=item_id)
    referred_from = request.META['HTTP_REFERER']
    qty = int(request.POST.get('qty'))

    if request.POST.get('qty') == '':
        messages.error(request, 'Invalid quantity', '')
        return redirect(referred_from)

    if product.qty_held < qty:
        messages.warning(request,
                         'Sorry! We could not update this item '
                         'qty in your cart. '
                         'We do not have the required amount '
                         'in stock.',
                         extra_tags='render_toast')
        return redirect(referred_from)

    cart = request.session.get('cart', {'products':{},'bundles':{},'custom_prints':{}})
    cart['products'][item_id] = qty
    extra_tags = 'render_toast render_preview'

    if 'cart' in referred_from:
        extra_tags = ''

    messages.info(
        request,
        f'Updated cart with {qty} x <strong>{product.name}</strong>!',
        extra_tags=extra_tags)

    request.session['cart'] = cart

    return redirect(referred_from)


def remove_product_from_cart(request, item_id):
    
    product = get_object_or_404(Product, pk=item_id)
    cart = request.session.get('cart', {'products':{},'bundles':{},'custom_prints':{}})
    referred_from = request.META['HTTP_REFERER']
    extra_tags = 'render_toast render_preview'

    if 'cart' in referred_from:
        extra_tags = ''

    if item_id in cart['products']:
        cart['products'].pop(item_id)
        messages.info(
            request,
            f'<strong>{product.name}</strong> removed from your cart!',
            extra_tags=extra_tags)

    request.session['cart'] = cart

    return redirect(referred_from)


def add_bundle_to_cart(request):
    
    # get referring url for redirect
    referred_from = request.META['HTTP_REFERER']
    
    # load the cart from the session
    cart = request.session.get('cart', {'products':{},'bundles':{},'custom_prints':{}})

    # load the template bundles
    orig_bundle_pk = int(request.POST.get('orig_bundle_pk'))
    orig_bundle = get_object_or_404(Bundle, pk=orig_bundle_pk)

    # generate new 'customised' bundle for this instance
    custom_bundle_id = uuid.uuid4().hex.upper() 
    custom_bundle = Bundle(
        bundle_id=custom_bundle_id,
        name=f'{request.user.username} {orig_bundle.name}',
        image=orig_bundle.image,
        category=BundleCategory.objects.get(name='custom'),
        custom=True,
    )
    custom_bundle.save(request.user.id)

    # get the customised bundle items of the request
    bundle_item_dict = get_bundle_item_dictionary(request.body)

    # validate the products in the bundle
    validated_products = validate_bundle_item_products(bundle_item_dict)
    if not validated_products['is_valid']:
        messages.error(request, 
                    getCannotProcessMessageProducts(
                        validated_products['product']),
                    extra_tags='render_toast')
        return redirect(referred_from)

    # validate the item qtys in the bundle
    validated = validate_bundle_item_qtys(bundle_item_dict)  
    if not validated['is_valid']:
        messages.error(request, 
                    getCannotProcessMessageQtys(
                        validated['product']),
                    extra_tags='render_toast')
        return redirect(referred_from)

    # if bundle is valid save the items
    save_bundle_items(bundle_item_dict, custom_bundle)

    # add to the cart
    cart['bundles'][custom_bundle_id] = 1 # handle qtys here in the future

    messages.success(
        request,
        f'Added your bundle to your cart!',
        extra_tags='render_toast render_preview')
    
    request.session['cart'] = cart

    return redirect('bundle_categories')


def update_bundle_in_cart(request, bundle_id):

    # get referring url for redirect
    referred_from = request.META['HTTP_REFERER']
    
    # load the cart from the session
    cart = request.session.get('cart', 
        {'products':{},'bundles':{},'custom_prints':{}})  

    # load the bundle to update
    bundle = get_object_or_404(Bundle, bundle_id=bundle_id)
    
    # get the customised bundle items of the request
    bundle_item_dict = get_bundle_item_dictionary(request.body)
  
    # validate the products in the bundle
    validated_products = validate_bundle_item_products(bundle_item_dict)
    if not validated_products['is_valid']:
        messages.error(request, 
                    getCannotProcessMessageProducts(
                        validated_products['product']),
                    extra_tags='render_toast')
        return redirect(referred_from)

    # validate the products in the bundle
    validated_qtys = validate_bundle_item_qtys(bundle_item_dict)
    if not validated_qtys['is_valid']:
        messages.error(request, 
                    getCannotProcessMessageQtys(validated_qtys['product']),
                    extra_tags='render_toast')
        return redirect(referred_from)

    # if updated bundle is valid then lets delete the current items 
    # in the bundle and replace them all 
    BundleItem.objects.filter(
        bundle__bundle_id=bundle_id).delete()
    save_bundle_items(bundle_item_dict, bundle)

    # update the cart
    cart['bundles'][bundle_id] = 1

    # if we are already in the cart view don't show toast
    extra_tags = 'render_toast render_preview'
    if 'cart' in referred_from:
        extra_tags = ''

    messages.info(
        request,
        f'Updated cart for <strong>{bundle.name}</strong>!',
        extra_tags=extra_tags)

    request.session['cart'] = cart
    
    return redirect(referred_from)


def remove_bundle_from_cart(request, bundle_id):
    
    # get referring url for redirect
    referred_from = request.META['HTTP_REFERER']

    # load the cart from the session
    cart = request.session.get('cart', 
        {'products':{},'bundles':{},'custom_prints':{}})
    
    # if we are already in the cart view don't show toast
    extra_tags = 'render_toast render_preview'
    if 'cart' in referred_from:
        extra_tags = ''

    # remove the item from the cart
    if bundle_id in cart['bundles']:
        cart['bundles'].pop(bundle_id)
        messages.info(
            request,
            f'Bundle removed from your cart!',
            extra_tags=extra_tags)

    request.session['cart'] = cart

    try:
        # try to delete items then the bundle
        BundleItem.objects.filter(
            bundle__bundle_id=bundle_id).delete()
        Bundle.objects.get(bundle_id=bundle_id).delete()
    except Bundle.DoesNotExist:
        return redirect(referred_from)

    return redirect(referred_from)
    


def add_or_update_custom_print_for_cart(request, custom_print_id):

    # load the cart from the session
    cart = request.session.get('cart', {'products':{},'bundles':{},'custom_prints':{}})

    custom_print_order = CustomPrintOrder.objects.get(pk=custom_print_id)

    if int(custom_print_order.base_product.qty_held) < int(custom_print_order.qty):
        messages.warning(request,
                         'Sorry! We could add this item to your cart. '
                         'We do not have the required amount '
                         'in stock.',
                         extra_tags='render_toast')
        HttpResponse(status=400, content=request)

    cart['custom_prints'][custom_print_id] = custom_print_order.qty

    request.session['cart'] = cart
    return HttpResponse(status=200, content=request)


def remove_custom_print_order_from_cart(request, custom_print_id):

    # get referring url for redirect
    referred_from = request.META['HTTP_REFERER']
    
    # load the cart from the session
    cart = request.session.get('cart', {'products':{},'bundles':{},'custom_prints':{}})
    
    # load the print_order to delete
    custom_print_order = get_object_or_404(CustomPrintOrder, pk=custom_print_id)

    # delete the 'custom print order as we no longer want it
    CustomPrintOrder.objects.filter(pk=custom_print_id).delete()
    
    # if we are already in the cart view don't show toast
    extra_tags = 'render_toast render_preview'
    if 'cart' in referred_from:
        extra_tags = ''

    # remove the item from the cart
    if custom_print_id in cart['custom_prints']:
        cart['custom_prints'].pop(custom_print_id)
        messages.info(
            request,
            f'Custom print order: <strong>{custom_print_order.base_product.name}</strong> removed from your cart!',
            extra_tags=extra_tags)

    request.session['cart'] = cart
     
    return redirect(referred_from)


''' helper functions '''


def validate_bundle_item_products(bundle_item_dict):
    product_ids = []
    valid = False
    for k, item in bundle_item_dict.items(): 
        if item['product'] != '0':
            product = Product.objects.get(pk=item['product'])
            if product.id in product_ids:
                return { 'is_valid': False, 'product': product }
            product_ids.append(product.id)
            valid = True # set when at least one item valid (i.e. cannot validate 0 bundle items) 
    return {'is_valid': valid, 'product': None }


def validate_bundle_item_qtys(bundle_item_dict):
    for k, item in bundle_item_dict.items(): 
        if item['product'] != '0':
            product = Product.objects.get(pk=item['product'])
            if (int(item['item_qty']) > product.qty_held or 
                int(item['item_qty']) == 0):
                return { 'is_valid': False, 'product': product }
    return { 'is_valid': True }


def save_bundle_items(bundle_item_dict, bundle): 
    for k, item in bundle_item_dict.items():
        if item['product'] != '0':
            product = Product.objects.get(pk=item['product'])
            bundle_item = BundleItem(
                product=product,
                bundle=bundle,
                item_qty=int(item['item_qty'])
            )
            bundle_item.save()


def get_bundle_item_dictionary(request_body):
    requestDictionary = request_body.decode("utf-8").split('&')
    return custom_formset_dictionary_parser(requestDictionary)


def getCannotProcessMessageProducts(product):
    msg = ''
    if product: 
        msg = f'''
            Invalid configuration of products, 
            more than one {product.name} 
            present in the bundle. 
            Please adjust your selections.
            '''
    else:
        msg = f'''
            No valid products in your bundle. 
            Please try again.
            '''
    return msg


def getCannotProcessMessageQtys(product):
    msg = ''
    if product.qty_held == 0:
        msg = f'''
        Sorry! We could not update your bundle. 
        We currently have no item <strong>{ product.name }</strong> 
        in stock!
        Please replace it with an alternative product.'''
    else:
        msg = f'''
        Sorry! We could not update your bundle. 
        The qty of item <strong>{ product.name }</strong> 
        is too high! 
        We only have { product.qty_held } in stock.'''
        
    return msg
            



