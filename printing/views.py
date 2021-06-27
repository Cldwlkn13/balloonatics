
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .models import CustomPrintOrder
from .forms import CustomPrintForm

from products.models import Product
from cart.views import add_or_update_custom_print_for_cart


def printing(request):

    return redirect(reverse('load_print_selector'))


def load_print_selector(request):
    
    products = Product.objects.filter(is_printable=True)

    # load up slideshow images
    slideshow_images = {
        'print-idea-1.jpg': 'Welcome someone home!',
        'print-idea-2.jpg': 'Say Happy Birthday',
        'print-idea-3.jpg': 'Some cool ideas!',
        'print-idea-4.jpg': 'Say a special Congratulaions!',
    }

    context = {
        'products': products,
        'cntxt': 'add',
        'slideshow_images': slideshow_images,
    }
    return render(request, 'printing/printing.html', context)


def new_order_handler(request):

    # get the printable balloons
    products = Product.objects.filter(is_printable=True)

    if request.method == 'POST':

        # get the product from the request
        try:
            p_id = int(request.POST.get('p_id'))
        except ValueError:
            messages.error(request,
                'Invalid Product. Please try another.',
                extra_tags='render_toast')
            return redirect(reverse('load_print_selector'))

        try:
            product = Product.objects.get(pk=p_id)
        except Product.DoesNotExist:
            messages.error(request,
                'Invalid Product. Please try another.',
                extra_tags='render_toast')
            return redirect(reverse('load_print_selector'))
        
        # get the custom message and qty from the request
        message = request.POST.get('custom_message')
        qty = request.POST.get('qty')

        # load and save a new custom print order
        custom_print_order = CustomPrintOrder(
            base_product=product,
            custom_message=message, 
            qty=qty
        )
        custom_print_order.save()

        # add it to the cart
        added_to_cart = add_or_update_custom_print_for_cart(
            request, custom_print_order.id).status_code == 200

        # error message triggered in add_or_update_custom_print_for_cart if fail
        if not added_to_cart:
            return redirect(reverse('load_print_selector'))

        messages.success(
            request,
            f'''Added print order for {custom_print_order.qty} x 
            <strong>{custom_print_order.base_product.name}</strong> 
            with message: "<i>{custom_print_order.custom_message}</i>"
            to your cart!''',
            extra_tags='render_toast render_preview')
        
        # load up the form with the data
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

    # if its not a product select request load up the selector form
    if not 'select_product' in request.GET:
        return redirect(reverse('load_print_selector'))
    
    # get id from request and try to get product 
    p_id = request.GET['select_product']   
    try:
        product = Product.objects.get(pk=p_id)
    except Product.DoesNotExist:
        messages.warning(request,
            'Please select a valid product',
            extra_tags='render_toast')
        return redirect(reverse('load_print_selector'))
    
    # load up an empty form
    order_form = CustomPrintForm('', 1)

    context = {
        'products': products,
        'order_form': order_form,
        'product': product,
        'cntxt': 'add',
    }
    return render(request, 'printing/printing.html', context)


def update_order_handler(request, custom_print_id):

    # get the referring url
    http_referrer = request.META['HTTP_REFERER']

    # load up the printable products
    products = Product.objects.filter(is_printable=True)
    
    if request.method == 'POST':
        # if product id not sent then load delector form
        if not 'p_id' in request.POST:
            return redirect(reverse('load_print_selector'))
        
        # get the product from the request
        p_id = request.POST.get('p_id')
        product = Product.objects.get(pk=p_id)

        # get the custom message and qty from the request
        message = request.POST.get('custom_message')
        qty = request.POST.get('qty')

        # try load up the print order from the request id
        try:
            custom_print_order = CustomPrintOrder.objects.get(
                pk=custom_print_id)
        except CustomPrintOrder.DoesNotExist:
            return redirect(reverse('load_print_selector'))
            
        # update the print order
        custom_print_order.base_product=product
        custom_print_order.custom_message=message
        custom_print_order.qty=qty
        custom_print_order.save()

        # update the order in the cart
        updated_in_cart = add_or_update_custom_print_for_cart(
            request, custom_print_id).status_code == 200
        
        # error message triggered in add_or_update_custom_print_for_cart if fail
        if not updated_in_cart:
            return redirect(reverse(http_referrer))

        messages.success(
            request,
            f'''Updated print order: {custom_print_order.qty} x 
            <strong>{custom_print_order.base_product.name}</strong> 
            with message: "<i>{custom_print_order.custom_message}</i>"
            to your cart!''',
            extra_tags='render_toast render_preview')
        
        # load up the form with the data
        order_form = CustomPrintForm(message, qty)
        
        context = {
            'products': products,
            'order_form': order_form,
            'product': product,
            'custom_print_order': custom_print_order,
            'cntxt': 'update',
        }
        return render(request, 'printing/printing.html', context)

    # if get request then try get the print order
    try:
        custom_print_order = CustomPrintOrder.objects.get(
            pk=custom_print_id)
    except CustomPrintOrder.DoesNotExist:
        return redirect(reverse('load_print_selector'))

    # load up the form with the data 
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

    