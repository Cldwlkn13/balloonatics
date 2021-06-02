from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm, AddressForm


def checkout(request):

    if request.method == 'POST':
        
        
        
        context = {
            'data': request.POST
        }
        return render(request, 'checkout/checkout-success.html', context)
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty")
            return redirect(reverse('products'))

        order_form = OrderForm()
        address_form = AddressForm()
        context = {
            'order_form': order_form,
            'address_form': address_form
        }

        return render(request, 'checkout/checkout.html', context)
