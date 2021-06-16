from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .models import CustomPrintedProduct
from .forms import ProductSelectorForm, CustomPrintForm

from products.models import Product, Category, Sub_Category

from datetime import datetime


def printing(request):

    return redirect(reverse('load_products'))


def load_print_selector(request):
    
    selector_form = ProductSelectorForm(0)

    context = {
        'selector_form': selector_form
    }
    return render(request, 'printing/printing.html', context)


def order(request):

    this_url = request.META['HTTP_REFERER']

    if request.method == 'POST':

        p_id = request.POST.get('p_id')
        product = Product.objects.get(pk=p_id)
        
        message = request.POST.get('custom_message')
        qty = request.POST.get('qty')

        custom_product = CustomPrintedProduct(
            base_product=product,
            user=request.user,
            custom_message=message, 
            qty=qty
        )
        custom_product.save()
        
        selector_form = ProductSelectorForm(p_id)
        order_form = CustomPrintForm(message, qty)
        
        context = {
            'selector_form': selector_form,
            'order_form': order_form,
            'product': product
        }
        return render(request, 'printing/printing.html', context)
    
    p_id = int(request.GET['select_product'])
    product = None
    
    try:
        product = Product.objects.get(pk=p_id)
    except Product.DoesNotExist:
        messages.warning(request,
            'Please select a valid product',
            extra_tags='render_toast')

        return redirect(reverse(this_url))
    
    selector_form = ProductSelectorForm(p_id)
    order_form = CustomPrintForm('', 1)
    
    context = {
        'selector_form': selector_form, 
        'order_form': order_form,
        'product': product
    }
    return render(request, 'printing/printing.html', context)