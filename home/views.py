from django.shortcuts import render
from django.http import HttpResponseForbidden, Http404,HttpResponseServerError, HttpResponseBadRequest
from products.models import Category, Sub_Category


def index(request):
    categories = Category.objects.all()
    sub_categories = Sub_Category.objects.all()

    slideshow_images_bundle = {
        'age_2_pink.jpg': 'Our Wedding Bundle',
        'mr_mrs.jpg': 'Our Wedding Bundle 2',
        'red-balloon.Jjpg': 'Our Wedding Bundle 3',
    }

    slideshow_images_printing = {
        'age_2_pink.jpg': 'Our Wedding Bundle',
        'mr_mrs.jpg': 'Our Wedding Bundle 2',
    }

    slideshow_images_event = {
        'age_2_pink.jpg': 'Our Wedding Bundle',
        'mr_mrs.jpg': 'Our Wedding Bundle 2',
        'leopard.jpg': 'Leopard yoke',
        'foil_A_lg.jpg': 'Our Wedding Bundle 4',
    }
    
    context = {
        'categories': categories, 
        'sub_cateogories': sub_categories,
        'slideshow_images_bundle': slideshow_images_bundle,
        'slideshow_images_printing': slideshow_images_printing,
        'slideshow_images_event': slideshow_images_event,
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