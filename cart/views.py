from django.shortcuts import render, redirect


def view_cart(request):

    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    
    qty = int(request.POST.get('qty'))
    this_url = request.POST.get('this_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += qty
    else:
        cart[item_id] = qty

    request.session['cart'] = cart
    return redirect(this_url)
