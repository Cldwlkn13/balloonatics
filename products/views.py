from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from .models import Product, Category, Sub_Category

import itertools


def products(request):

    products = Product.objects.all()

    context = {
        "products": products,
    }

    return render(request, 'products/products.html', context)


def categories(request):

    categories = Category.objects.all()

    context = {
        "categories": categories,
    }

    return render(request, 'products/categories.html', context)


def sub_categories(request):

    sub_categories = Sub_Category.objects.all()

    if 'category' in request.GET:
        category = request.GET['category']
        matching_sub_categories = Product.objects.filter(category__name=category).distinct().values('sub_category')
        sub_category_pks = []
        for i in matching_sub_categories:
            for y in i.values():
                sub_category_pks.append(y)

        sub_categories = Sub_Category.objects.filter(id__in=sub_category_pks)

    context = {
        "sub_categories": sub_categories,
        'b': 'true'
    }

    return render(request, 'products/sub_categories.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
