
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .models import CustomPrintOrder
from .forms import ProductSelectorForm, CustomPrintForm

from products.models import Product
from cart.views import add_or_update_custom_print_for_cart


def printing(request):

    return redirect(reverse('load_print_selector'))


def load_print_selector(request):
    
    products = Product.objects.filter(is_printable=True)

    context = {
        'products': products,
        'cntxt': 'add'
    }
    return render(request, 'printing/printing.html', context)


def new_order_handler(request):

    http_referrer = request.META['HTTP_REFERER']

    products = Product.objects.filter(is_printable=True)

    if request.method == 'POST':

        p_id = int(request.POST.get('p_id'))
        product = Product.objects.get(pk=p_id)
        
        message = request.POST.get('custom_message')
        qty = request.POST.get('qty')

        custom_print_order = CustomPrintOrder(
            base_product=product,
            custom_message=message, 
            qty=qty
        )
        custom_print_order.save()

        added_to_cart = add_or_update_custom_print_for_cart(
            request, custom_print_order.id).status_code == 200

        if not added_to_cart:
            return redirect(reverse('load_print_selector'))

        messages.success(
            request,
            f'''Added print order for {custom_print_order.qty} x 
            <strong>{custom_print_order.base_product.name}</strong> 
            with message: "<i>{custom_print_order.custom_message}</i>"
            to your cart!''',
            extra_tags='render_toast render_preview')
        
        order_form = CustomPrintForm(message, qty)
        
        context = {
            'products': products,
            'order_form': order_form,
            'product': product,
            'custom_print_order': custom_print_order,
            'cntxt': 'update'
        }
        return render(request, 'printing/printing.html', context)
    
    product = None

    if not 'select_product' in request.GET:
        return redirect(reverse('load_print_selector'))
    
    p_id = request.GET['select_product']
    
    try:
        product = Product.objects.get(pk=p_id)
    except Product.DoesNotExist:
        messages.warning(request,
            'Please select a valid product',
            extra_tags='render_toast')

        return redirect(reverse('load_print_selector'))
    
    order_form = CustomPrintForm('', 1)

    context = {
        'products': products,
        'order_form': order_form,
        'product': product,
        'cntxt': 'add',
    }
    return render(request, 'printing/printing.html', context)


def update_order_handler(request, custom_print_id):

    http_referrer = request.META['HTTP_REFERER']

    products = Product.objects.filter(is_printable=True)
    
    if request.method == 'POST':
        if not 'p_id' in request.POST:
            return redirect(reverse('load_print_selector'))
        
        p_id = request.POST.get('p_id')
        product = Product.objects.get(pk=p_id)

        message = request.POST.get('custom_message')
        qty = request.POST.get('qty')

        try:
            custom_print_order = CustomPrintOrder.objects.get(
                pk=custom_print_id)
        except CustomPrintOrder.DoesNotExist:
            return redirect(reverse('load_print_selector'))
            
        custom_print_order.base_product=product
        custom_print_order.custom_message=message
        custom_print_order.qty=qty
        custom_print_order.save()

        updated_in_cart = add_or_update_custom_print_for_cart(
            request, custom_print_id).status_code == 200
        
        if not updated_in_cart:
            return redirect(reverse(http_referrer))

        messages.success(
            request,
            f'''Updated print order: {custom_print_order.qty} x 
            <strong>{custom_print_order.base_product.name}</strong> 
            with message: "<i>{custom_print_order.custom_message}</i>"
            to your cart!''',
            extra_tags='render_toast render_preview')
        
        order_form = CustomPrintForm(message, qty)
        
        context = {
            'products': products,
            'order_form': order_form,
            'product': product,
            'custom_print_order': custom_print_order,
            'cntxt': 'update',
        }
        return render(request, 'printing/printing.html', context)

    try:
        custom_print_order = CustomPrintOrder.objects.get(
            pk=custom_print_id)
    except CustomPrintOrder.DoesNotExist:
        return redirect(reverse('load_print_selector'))

    order_form = CustomPrintForm(custom_print_order.custom_message, 
        custom_print_order.qty)
    
    context = {
        'products': products,
        'order_form': order_form,
        'product': custom_print_order.base_product,
        'custom_print_order': custom_print_order,
        'cntxt': 'update',
    }
    
    return render(request, 'printing/printing.html', context)

    