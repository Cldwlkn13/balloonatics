from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from products.models import Product


def view_cart(request):

    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):

    product = get_object_or_404(Product, pk=item_id)
    qty = int(request.POST.get('qty'))
    this_url = request.POST.get('this_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += qty
    else:
        cart[item_id] = qty

    messages.success(
        request,
        f'Added {qty} x <strong>{product.name}</strong> to your cart!',
        extra_tags='render_preview')

    request.session['cart'] = cart
    return redirect(this_url)


def update_cart(request, item_id):

    product = get_object_or_404(Product, pk=item_id)
    path = request.POST.get('this_url')

    if request.POST.get('qty') == '':
        messages.error(request, 'Invalid quantity', '')
        return redirect(path)

    qty = int(request.POST.get('qty'))

    cart = request.session.get('cart', {})
    cart[item_id] = qty
    extra_tags = ''

    if 'cart' not in path:
        extra_tags = 'render_preview'

    messages.info(
        request,
        f'Updated cart with {qty} x <strong>{product.name}</strong>!',
        extra_tags=extra_tags)

    request.session['cart'] = cart
    return redirect(path)


def remove_from_cart(request, item_id):

    product = get_object_or_404(Product, pk=item_id)
    cart = request.session.get('cart', {})
    path = request.META['HTTP_REFERER']
    extra_tags = ''

    if 'cart' not in path:
        extra_tags = 'render_preview'

    if item_id in cart:
        cart.pop(item_id)
        messages.info(
            request,
            f'<strong>{product.name}</strong> removed from your cart!',
            extra_tags=extra_tags)

    request.session['cart'] = cart
    return redirect(path)
