from django.shortcuts import (render, redirect, reverse,
                              HttpResponse)
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST

from .forms import OrderForm, AddressForm
from .models import Order, OrderItem, Address
from products.models import Product
from profiles.models import UserProfile
from profiles.forms import ProfileForm
from cart.contexts import cart_contents

import stripe
import json
import uuid


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again later.'))
        return HttpResponse(content=e, status=400)


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
                street_address_1=address_form_data['street_address_1'],
                street_address_2=address_form_data['street_address_2'],
                city_town=address_form_data['city_town'],
                county_area=address_form_data['county_area'],
                country=address_form_data['country'],
                postal_code=address_form_data['postal_code'])
            order_id = uuid.uuid4().hex.upper()
            order = Order(order_id=order_id,
                          cust_name=order_form_data['cust_name'],
                          cust_email=order_form_data['cust_email'],
                          cust_phone=order_form_data['cust_phone'],
                          address=address)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
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
                        "Please contact us for assistance",
                        extra_tags='render_toast')
                    order.delete()
                    return redirect(reverse('view_cart'))

            request.session['save_info'] = 'save-info' in request.POST

            return redirect(reverse('checkout_success',
                                    args=[order_id]))
        else:
            messages.error(request,
                           "Your form could not be processed. "
                           "Please check your information and try "
                           "again",
                           extra_tags='render_toast')
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty",
                           extra_tags='render_toast')
            return redirect(reverse('products'))

        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = None
        address_form = None
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'cust_name': profile.cust_name,
                    'cust_email': profile.cust_email,
                    'cust_phone': profile.cust_phone,
                })
                address_form = AddressForm(initial={
                    'street_address_1': profile.street_address_1,
                    'street_address_2': profile.street_address_2,
                    'city_town': profile.city_town,
                    'county_area': profile.county_area,
                    'country': profile.country,
                    'postal_code': profile.postal_code,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
                address_form = AddressForm()
        else:
            order_form = OrderForm()
            address_form = AddressForm()

        context = {
            'order_form': order_form,
            'address_form': address_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret
        }

        return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_id):
    order = None
    order_items = None

    try:
        order = list(Order.objects.filter(order_id=order_id))[0]
        order_items = list(OrderItem.objects.filter(order__order_id=order_id))
    except Exception:
        messages.error(request,
                       'Could not confirm success of your Order '
                       'Please contact us to confirm. ',
                       extra_tags='render_toast')
        return redirect(reverse('checkout'))

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

        profile_data = {
            'cust_name': order.cust_name,
            'cust_email': order.cust_email,
            'cust_phone': order.cust_phone,
            'street_address_1': order.address.street_address_1,
            'street_address_2': order.address.street_address_2,
            'city_town': order.address.city_town,
            'county_area': order.address.county_area,
            'country': order.address.country,
            'postal_code': order.address.postal_code
        }

        save_info = request.session.get('save_info')
        if save_info:
            user_profile_form = ProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

        if 'cart' in request.session:
            del request.session['cart']

        context = {
            'order': order,
            'order_items': order_items
        }

        return render(request, 'checkout/checkout_success.html', context)
