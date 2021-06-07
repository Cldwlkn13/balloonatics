from django.shortcuts import (render, get_object_or_404,
                              redirect, reverse, HttpResponse)
from django.db.models.functions import Lower
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Product, Category, Sub_Category
from .forms import ProductForm, ProductSelectorForm


def products(request):
    products = Product.objects.all()
    sub_category = 'all'
    sort = None
    direction = None

    if 'sub_category' in request.GET:
        sub_category = request.GET['sub_category']
        products = Product.objects.filter(sub_category__name=sub_category)

    if 'sort' in request.GET:
        sortkey = request.GET['sort']
        sort = sortkey
        if sortkey == 'name':
            sortkey = 'lower_name'
            products = products.annotate(lower_name=Lower('name'))
        if 'dir' in request.GET:
            direction = request.GET['dir']
            if direction == 'desc':
                sortkey=f'-{sortkey}'
        products = products.order_by(sortkey)

    cart = request.session.get('cart', {})

    for product in products:
        product.qty_in_cart = product.calc_qty_in_bag(cart)

    context = {
        "products": products,
        'sub_category': sub_category,
        'current_sort': sort,
        'current_dir': direction,
        'product_alert_qty_threshold': settings.QTY_LOW_ALERT_THRESHOLD,
    }

    return render(request, 'products/products.html', context)


def categories(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return render(request, 'products/categories.html', context)


def sub_categories(request):
    sub_categories = Sub_Category.objects.all()

    if 'category' in request.GET:
        category = request.GET['category']
        matching_sub_categories = Product.objects.filter(category__name=category).distinct().values('sub_category')
        sub_category_pks = []
        for sc in matching_sub_categories:
            for v in sc.values():
                sub_category_pks.append(v)

        sub_categories = Sub_Category.objects.filter(id__in=sub_category_pks)

    context = {
        "sub_categories": sub_categories,
        'category': category
    }

    return render(request, 'products/sub_categories.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})
    qty_in_cart = product.calc_qty_in_bag(cart)
    product.qty_in_cart = qty_in_cart

    context = {
        'product': product,
        'product_alert_qty_threshold': settings.QTY_LOW_ALERT_THRESHOLD,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def load_products(request):
    selector_form = ProductSelectorForm()

    context = {
        'selector_form': selector_form
    }
    return render(request, 'products/load_products.html', context)


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request,
                             f'Successfully added product: {product.name}!',
                             extra_tags='render_toast')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request,
                           f'Error adding product: {product.name} '
                           'Please check the form and try again.',
                           extra_tags='render_toast')
    else:
        form = ProductForm()
        bundle_form = BundleItemForm()

    context = {
        'form': form,
        'bundle_form': bundle_form
    }

    return render(request, 'products/add_product.html', context)


@login_required
def edit_product(request):
    if not request.user.is_superuser:
        messages.error(request,
                       'Please log in with your store owner account',
                       extra_tags='render_toast')
        return redirect(reverse('home'))

    if request.method == 'POST':
        p_id = request.POST['p_id']
        product = get_object_or_404(Product, pk=p_id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Successfully updated product!',
                             extra_tags='render_toast')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            form = ProductForm(instance=product)
    else:
        p_id = int(request.GET['select_product'])
        if p_id != 0:
            product = get_object_or_404(Product, pk=p_id)
            form = ProductForm(instance=product)
        else:
            form = ProductForm()

    context = {
        'form': form,
        'product': product,
    }

    return render(request, 'products/edit_product.html', context)


@login_required
def delete_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request,
                       'Please log in with your store owner account',
                       extra_tags='render_toast')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request,
                     f'{product.name} has been deleted!',
                     extra_tags='render_toast')
    return redirect(reverse('load_products'))


