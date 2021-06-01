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
        messages.success(request, f'Added {product.name} to your bag!')

    request.session['cart'] = cart
    return redirect(this_url)


def update_cart(request, item_id):

    this_url = request.POST.get('this_url')

    if request.POST.get('qty') == '':
        return redirect(this_url)

    qty = int(request.POST.get('qty'))

    cart = request.session.get('cart', {})
    cart[item_id] = qty

    request.session['cart'] = cart
    return redirect(this_url)


def remove_from_cart(request, item_id):

    cart = request.session.get('cart', {})

    cart.pop(item_id)

    request.session['cart'] = cart
    return render(request, 'cart/cart.html')