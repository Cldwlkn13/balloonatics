from django.shortcuts import render, get_object_or_404
from django.db.models.functions import Lower

from .models import Product, Category, Sub_Category


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
        'current_dir': direction
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
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})
    qty_in_cart = product.calc_qty_in_bag(cart)
    product.qty_in_cart = qty_in_cart

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
