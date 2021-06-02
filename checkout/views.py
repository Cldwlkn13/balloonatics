from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm, AddressForm
from .models import Order, OrderItem, Address
from products.models import Product
from cart.contexts import cart_contents

import stripe
import json
import uuid


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    cart = request.session.get('cart', {})
    if request.method == 'POST':

        address_form_data = {
            'street_address_1': request.POST['street_address_1'],
            'street_address_2': request.POST['street_address_2'],
            'city_town': request.POST['city_town'],
            'county_area': request.POST['county_area'],
            'country': request.POST['country'],
            'postal_code': request.POST['postal_code'],
        }

        order_form_data = {
            'cust_name': request.POST['cust_name'],
            'cust_email': request.POST['cust_email'],
            'cust_phone': request.POST['cust_phone'],
        }

        address_form = AddressForm(address_form_data)
        order_form = OrderForm(order_form_data)

        if address_form.is_valid() and order_form.is_valid():
            address = Address(
                street_address_1=address_form['street_address_1'],
                street_address_2=address_form['street_address_2'],
                city_town=address_form['city_town'],
                county_area=address_form['county_area'],
                country=address_form['country'],
                postal_code=address_form['postal_code'])
            order_id = uuid.uuid4().hex.upper()
            order = Order(order_id=order_id,
                          cust_name=order_form['cust_name'],
                          cust_email=order_form_data['cust_email'],
                          cust_phone=order_form_data['cust_phone'],
                          address=address)
            order.save()
            for item_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_item = OrderItem(order=order,
                                           product=product,
                                           quantity=item_data)
                    order_item.save()
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        f"Product with id {item_id} could not be processed "
                        "Please contact us for assistance")
                    order.delete()
                    return redirect(reverse('view_cart'))

            request.session['save_info'] = 'save-info' in request.POST

            context = {
                'order': order
            }

            return render(request, 'checkout/checkout-success.html', context)
        else:
            messages.error(request, ("Your form could not be processed. "
                                     "Please check your information and try "
                                     "again"))
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty")
            return redirect(reverse('products'))

        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()
        address_form = AddressForm()
        context = {
            'order_form': order_form,
            'address_form': address_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': '3'
        }

        return render(request, 'checkout/checkout.html', context)
