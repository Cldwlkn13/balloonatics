from django.shortcuts import render
from django.http import HttpResponseForbidden, Http404,HttpResponseServerError, HttpResponseBadRequest
from products.models import Category, Sub_Category


def index(request):
    categories = Category.objects.all()
    sub_categories = Sub_Category.objects.all()

    context = {
        'categories': categories, 
        'sub_cateogories': sub_categories 
    }

    return render(request, 'home/index.html', context)


def bad_request_view(request, exception):

    context = {
        'exception': exception
    }
    
    return render(request, '400.html', context)

def permission_denied_view(request, exception):

    context = {
        'exception': exception
    }
    
    return render(request, '403.html', context)

def page_not_found_view(request, exception):

    context = {
        'exception': exception
    }
    
    return render(request, '404.html', context)


def error_view(request):
    
    return render(request, '500.html')