from django.shortcuts import render
from products.models import Category, Sub_Category


def index(request):
    categories = Category.objects.all()
    sub_categories = Sub_Category.objects.all()

    context = {
        'categories': categories, 
        'sub_cateogories': sub_categories 
    }

    return render(request, 'home/index.html', context)