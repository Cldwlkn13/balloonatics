from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta, timezone

from products.models import Product
from .models import Order, OrderItem, Address
from profiles.models import UserProfile

import json
import time


class StripeWH_Handler:

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        return HttpResponse(
            content=f'Unhandled Webhook Received: {event.type}',
            status=200
        )

    def _send_confirmation_order(self, order):
        cust_email = order.cust_email
        subject = render_to_string(
            './confirmation_emails/confirmation_email_subject.txt',
            {
                'order': order
            })
        body = render_to_string(
            './confirmation_emails/confirmation_email_body.txt',
            {
                'order': order,
                'contact_email': settings.DEFAULT_FROM_EMAIL
            })

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_payment_intent_succeeded(self, event):

        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)
        
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.phone_number = shipping_details.phone
                profile.street_address_1 = shipping_details.address.line1
                profile.street_address_2 = shipping_details.address.line2
                profile.city_town = shipping_details.address.city
                profile.county_area = shipping_details.address.state
                profile.country = shipping_details.address.country
                profile.postal_code = shipping_details.address.postal_code
                profile.save()

        order_exists = False
        attempt = 1
        """
            for customers with multiple orders in the system we only want
            to retrieve an order that was submitted within the past 10s
        """
        utc_dt = datetime.now(timezone.utc) 
        dt_threshold = utc_dt.astimezone() - timedelta(seconds=10)
        time.sleep(1)
        while attempt <= 5:
            orders = list(Order.objects.filter(
                cust_name__iexact=shipping_details.name,
                cust_email__iexact=billing_details.email,
                cust_phone__iexact=shipping_details.phone,
                grand_total=grand_total,
                original_cart=cart,
                stripe_pid=pid,
            ).order_by('-date'))
            orders = [order for order in orders if order.date > dt_threshold]
            if orders:
                order = orders[0]
                order_exists = True
                address = Address.objects.create(
                    street_address_1=shipping_details.address.line1,
                    street_address_2=shipping_details.address.line2,
                    city_town=shipping_details.address.city,
                    county_area=shipping_details.address.state,
                    country=shipping_details.address.country,
                    postal_code=shipping_details.address.postal_code
                )
                order.address = address
                break
            else:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_order(order)
            return HttpResponse(
                content=(f'Webhook received: {event["type"]} | SUCCESS: '
                         'Verified order already in database'),
                status=200)
        else:
            order = None
            try:
                address = Address.objects.create(
                    street_address_1=shipping_details.address.line1,
                    street_address_2=shipping_details.address.line2,
                    city_town=shipping_details.address.city,
                    county_area=shipping_details.address.state,
                    country=shipping_details.address.country,
                    postal_code=shipping_details.address.postal_code
                )
                order = Order.objects.create(
                    cust_name=billing_details.name,
                    cust_email=billing_details.email,
                    cust_phone=billing_details.phone,
                    address=address,
                    original_cart=cart,
                    stripe_pid=pid
                )
                for item_id, item_data in json.loads(cart).items():
                    product = Product.objects.get(id=item_id)
                    order_item = OrderItem(
                        order=order,
                        product=product,
                        quantity=item_data
                    )
                    product.qty_held -= item_data
                    product.save()
                    order_item.save()
                    
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

        self._send_confirmation_order(order)
        return HttpResponse(
            content=(f'Webhook received: {event["type"]} | SUCCESS: '
                     'Created order in webhook'),
            status=200)

    def handle_payment_intent_failed(self, event):
        return HttpResponse(
            content=f'Received: {event["type"]}',
            status=200
        )
